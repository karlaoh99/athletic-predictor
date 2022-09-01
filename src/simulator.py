import joblib
import dill
import numpy as np

from typing import List, Dict
from pathlib import Path
from competition_data import CompetitionData
from sklearn.neighbors import KernelDensity


def _create_kde_model(results: np.ndarray, bandwidth: float) -> KernelDensity:
    model = KernelDensity(bandwidth=bandwidth, kernel='gaussian')
    model.fit(X = results.reshape((-1,1)))
    return model

    # results_range = np.max(results) - np.min(results)
    # half_range = results_range / 2

    # param_grid = {
    #     'kernel': ['gaussian'],
    #     'bandwidth' : np.linspace(1e-3, half_range, 100)
    # }

    # grid = GridSearchCV(
    #         estimator  = KernelDensity(),
    #         param_grid = param_grid,
    #         n_jobs     = -1,
    #         cv         = 10,
    #         verbose    = 0
    #     )

    # grid.fit(X = results.reshape((-1,1)))
    # model: KernelDensity = grid.best_estimator_
    # return model


def _create_event_models(event_data: dict, event: str, sex: str, bandwidth: float, save_folder: str = None,
                        override_models: bool = False, logs: bool = False) -> Dict[str, KernelDensity]:
    
    if logs:
        print(f'Creating models for event {event} and sex {sex}...')

    models = {}
    athletes_name = event_data.keys()
    for i, name in enumerate(athletes_name):
        if logs:
            percent = (i + 1) * 100 / len(athletes_name)
            print(f'({percent:.2f} %) Creating kde model of {name}...')
        
        results = event_data[name].Result.to_numpy()
        model = _create_kde_model(results, bandwidth)
        
        if save_folder is not None:
            folder_path = Path(save_folder)
            folder_path.mkdir(parents=True, exist_ok=True)
            full_path = folder_path / f'{name}.pkl'

            if full_path.exists() and not override_models:
                if logs:
                    print(f'    Model already exist.')
                model = joblib.load(full_path)
            else:
                with open(full_path, 'wb') as f:
                    dill.dump(model, f)
        
        models[name] = model
    
    return models


def _get_ith_place(places, i, fst_positions):
    record = np.zeros(places.shape[1], dtype=int)

    for place in places:        
        for j in range(i+1):
            if place[j] in fst_positions:
                continue
            
            record[place[j]] += 1
            break

    return np.argmax(record)


def _run_simulation(names: List[str], models: List[KernelDensity], times: int, maximize: bool) -> List[str]:
    indices = {name: i for i, name in enumerate(names)}
    count = len(names)
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
        order.append(_get_ith_place(places, i, order))

    return [names[i] for i in order]


def simulate_event(data: dict, event: str, sex: str, competition: CompetitionData, times: int, models_folder: str = None, 
                   override_models: bool = False, logs: bool = False):
    
    bandwidth = competition.get_event_param(event, sex, 'bw', None)
    sim_times = competition.get_event_param(event, sex, 'sim_times', times)

    if models_folder is not None:
        event_folder = Path(models_folder) / Path(event) / Path(sex)
        models_folder = str(event_folder)

    event_models = _create_event_models(data, event, sex, bandwidth, models_folder, override_models, logs=logs)
    
    models = []
    names = []
    for name, model in event_models.items():
        models.append(model)
        names.append(name)

    if logs:
        print(f'Simulating event: {event}. Sex: {sex}...')
    
    return _run_simulation(names, models, sim_times, competition.is_maximize_event(event))


def simulate_all_events(data: dict, competition: CompetitionData, top: int = 3, times: int = 30, only: List[str] = None, logs: bool = False) -> dict:
    predictions = {}
    
    for event in competition.events:
        if only is not None and event not in only:
            continue
        
        if event not in data:
            if logs:
                print(f"[WARNING] Event data for '{event}' not found")
            continue
        
        predictions[event] = {}
        event_name = competition.get_event_data(event)['name']
        
        for sex in competition.get_event_data(event)['sex']:            
            if sex not in data[event]:
                if logs:
                    print(f"[WARNING] '{sex}' data for event '{event_name}' not found")
                continue
            
            result = simulate_event(
                data = data[event][sex], 
                event = event, 
                sex = sex, 
                competition=competition,
                times = times, 
                models_folder='models',
                override_models = True,
                logs = logs)
            
            if logs:
                if not result:
                    print('Simulation failed')
                    continue
                
                print(f'Resuts:')
                for i, name in enumerate(result[:top]):
                    print(f'{i + 1:>3}: {name}')
        
            predictions[event][sex] = result

    return predictions