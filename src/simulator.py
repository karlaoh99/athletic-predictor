import json
import os
from pathlib import Path
from typing import List
import joblib

import numpy as np
from prediction_saver import get_country_nd_name
from events_data import events, maximize_events, events_in_groups, get_event_param

# Ajuste de distribuciones
# ==============================================================================
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV


def model_by_cross_validation(results: np.ndarray, current_bandwith = None) -> KernelDensity:
    if current_bandwith is not None:
        model = KernelDensity(bandwidth=current_bandwith, kernel='gaussian')
        model.fit(X = results.reshape((-1,1)))
        return model

    results_range = np.max(results) - np.min(results)
    half_range = results_range / 2

    param_grid = {
        'kernel': ['gaussian'],
        'bandwidth' : np.linspace(1e-3, half_range, 100)
    }

    grid = GridSearchCV(
            estimator  = KernelDensity(),
            param_grid = param_grid,
            n_jobs     = -1,
            cv         = 10,
            verbose    = 0
        )

    grid.fit(X = results.reshape((-1,1)))
    model: KernelDensity = grid.best_estimator_
    return model


def athlete_kde_model(event_data, athlete_name, current_bandwith):
    df = event_data[athlete_name]
    results = df.Result.to_numpy()
    return model_by_cross_validation(results, current_bandwith)


def event_models(event_data, event_name: str, sex: str, save_folder: str = None,
                 logs: bool = True) -> List[KernelDensity]:
    print('Calculating models')
    athlete_names_results = [(name, result.Result.to_numpy()) for name, result in event_data.items()]
    marks_count_mean = np.mean([len(x[1]) for x in athlete_names_results if len(x[1]) >= 10])
    athlete_names_results.sort(key = lambda x : abs(len(x[1]) - marks_count_mean))
    athlete_names = [x[0] for x in athlete_names_results]

    current_bandwith = get_event_param(event_name, sex, 'bw', None)
    models = []

    # proxecutor = ThreadPoolExecutor()
    # tasks = [proxecutor.submit(single_model, event_name, sex, name, save_folder, models) for name in athlete_names]
    # wait(tasks, return_when=ALL_COMPLETED)
    for i, name in enumerate(athlete_names):
        if logs:
            # clear_output(wait=True)
            percent = ((i + 1) * 100) / len(athlete_names)
            print(f'({percent:.2f} %) Creating kde model of {name}...')
        model = None
        if save_folder is not None:
            folder_path = Path(save_folder)
            folder_path.mkdir(parents=True, exist_ok=True)
            full_path = folder_path / f'{name}.pkl'
            # if full_path.exists():
            #     if logs:
            #         print(f'    Model already exist')
            #     model = joblib.load(full_path)
            # else:
            model = athlete_kde_model(event_data, name, current_bandwith)
            current_bandwith = model.bandwidth
            joblib.dump(model, full_path)
        else:
            model = athlete_kde_model(event_data, name, current_bandwith)
            current_bandwith = model.bandwidth
        models.append(model)
    return models


def load_entry_json() -> dict:
    try:
        with open('entry_list.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except: 
        return None


def get_ith_place(places, i, fst_positions):
    record = np.zeros(places.shape[1], dtype=int)

    for place in places:        
        for j in range(i+1):
            if place[j] in fst_positions:
                continue
            
            record[place[j]] += 1
            break

    return np.argmax(record)


def run_simulation(names: List[str], models: List[KernelDensity], times=30, maximize=False):
    indices = {name:i for i, name in enumerate(names)}
    count = len(names)
    print(count)
    print(times)
    places = np.zeros((times, count), dtype=int)

    for t in range(times):
        sim = [(model.sample(), name) for name, model in zip(names, models)]
        sim.sort(key = lambda x: x[0][0], reverse=maximize)
        for i, tup in enumerate(sim):
            _, name = tup
            places[t][i] = indices[name]

    #get first place
    record = np.zeros(count, dtype=int)
    for place in places:
        record[place[0]] += 1

    first_place = np.argmax(record)
    
    order = [first_place]
    for i in range(1, count):
        order.append(get_ith_place(places, i, order))

    return [names[i] for i in order]


def simulate_event(event_data, event, sex, times, models_folder: str = None, override_models: bool = False, logs: bool = True):
    event_folder = Path(models_folder) / Path(event) / Path(sex)
    event_folder_str = str(event_folder)

    if models_folder is None:
        event_models(event_data, event, sex, logs=logs)
    elif not event_folder.exists() or override_models:
        event_models(event_data, event, sex, event_folder_str, logs=logs)
    
    entry_list = load_entry_json()

    models = []
    names = []
    for root, _, files in os.walk(event_folder_str):
        for file in files:
            if file.endswith('.pkl'):
                name = file.split('.')[0]

                if not event in events_in_groups:
                    _, name = get_country_nd_name(name)                

                if entry_list is not None and not name.casefold() in entry_list[event][sex]:
                    continue

                names.append(file.split('.')[0])
                full_path = str(Path(root) / Path(file))
                model = joblib.load(full_path)
                models.append(model)

    print('Simulating')
    maximize = event in maximize_events
    return run_simulation(names, models, times, maximize)


not_sim_events = ['atl_4x100m','atl_4x400m']


def simulate_all(events_data, top=3, times=30, logs=True, warnings=False, only=None):
    predictions = {}
    
    for event in events:
        if only is not None and event not in only:
            continue

        if event in not_sim_events:
            continue
        
        predictions[event] = {}
        event_name = events[event]['name']

        # Event data not extracted
        if event not in events_data:
            if logs and warnings:
                print(f"[WARNING] Event data for '{event_name}' not found")
            continue
        
        for sex in events[event]['sex']:
            sim_times = get_event_param(event, sex, 'sim_times', times)
            if sex not in events_data[event]:
                if logs and warnings:
                    print(f"[WARNING] '{sex}' data for event '{event_name}' not found")
                continue

            if logs:
                print(f'Simulating event: {event_name}. Sex: {sex}')
            
            result = simulate_event(
                event_data = events_data[event][sex], 
                event = event, 
                sex = sex, 
                times = sim_times, 
                models_folder='models',
                logs = logs)
            
            if logs:
                if not result:
                    print('Failed')
                    continue
                else:
                    print(f'Resuts:')
                    print_sim_result(result, top=top)
            
            predictions[event][sex] = result

    return predictions


def print_sim_result(sim_result: List[str], top: int = None):
    if top is None:
        top = len(sim_result)
    for i, name in enumerate(sim_result[:top]):
        print(f'{i + 1:>3}: {name}')