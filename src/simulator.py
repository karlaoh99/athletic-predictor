import joblib
import dill
import numpy as np
from typing import List, Dict
from pathlib import Path
from sklearn.neighbors import KernelDensity
from src.competition_data import CompetitionData


def _create_kde_model(results: np.ndarray, bandwidth: float) -> KernelDensity:
    model = KernelDensity(bandwidth=bandwidth, kernel='gaussian')
    model.fit(X = results.reshape((-1,1)))
    return model


def _create_event_models(event_data: dict, bandwidth: float, save_folder: str = None,
                        override_models: bool = True, logs: bool = False) -> Dict[str, KernelDensity]:

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
                    print(f'    Loading model that already exist...')
                model = joblib.load(full_path)
            else:
                with open(full_path, 'wb') as f:
                    dill.dump(model, f)
        
        models[name] = model
    
    return models


def _get_ith_place(places: np.array, i: int, fst_positions: List[int]) -> int:
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
                   override_models: bool = True, logs: bool = False) -> List[str]:
    """Simulates an event.

    Parameters
    ----------
    data : dict
        Athletes marks of an event and gender
    event : str
        Event name
    sex : str
        Event gender
    competition : CompetitionData
        Contains the data of the competition
    times : int
        Number of times to do the simulation
    models_folder : str, optional
        The folder where to store the models created or from where to load them  
    override_models : bool, optional
        True if old models want to be loaded
    logs : bool, optional
        True if logs want to be shown

    Returns
    -------
    List[str]
        The final result of the simulation
    """

    bandwidth = competition.get_event_param(event, sex, 'bw', 1)
    sim_times = competition.get_event_param(event, sex, 'sim_times', times)

    if models_folder is not None:
        event_folder = Path(models_folder) / Path(event) / Path(sex)
        models_folder = str(event_folder)

    if logs:
        print(f'Creating athletes models for event {event} and sex {sex}...')
    event_models = _create_event_models(data, bandwidth, models_folder, override_models, logs)
    
    models = []
    names = []
    for name, model in event_models.items():
        models.append(model)
        names.append(name)

    if logs:
        print(f'Simulating event: {event}. Sex: {sex}...')
    
    return _run_simulation(names, models, sim_times, competition.is_maximize_event(event))


def simulate_all_events(data: dict, competition: CompetitionData, top: int = 3, times: int = 30, models_folder: str = None, 
                        override_models: bool = True, only: List[str] = None, logs: bool = False) -> dict:
    """Simulates all the events.

    Parameters
    ----------
    data : dict
        Athletes marks of each event and gender
    competition : CompetitionData
        Contains the data of the competition
    top : int, optional
        Number of positions in the result to log
    times : int, optional
        Number of times to do the simulation
    models_folder : str, optional
        The folder where to store the models created or from where to load them  
    override_models : bool, optional
        True if old models want to be loaded
    only : List[str], optional
        Contains the events that are going to be simulated
    logs : bool, optional
        True if logs want to be shown

    Returns
    -------
    dict
        The final result of the simulation for each event and gender
    """

    predictions = {}
    
    for event in competition.events:
        if only is not None and event not in only:
            continue
        
        if event not in data:
            if logs:
                print(f"[WARNING] Event data for '{event}' not found")
            continue
        
        predictions[event] = {}
        for sex in competition.get_event_data(event)['sex']:            
            if sex not in data[event]:
                if logs:
                    print(f"[WARNING] '{sex}' data for event '{event}' not found")
                continue
            
            result = simulate_event(
                data=data[event][sex], 
                event=event, 
                sex=sex, 
                competition=competition,
                times=times, 
                models_folder=models_folder,
                override_models=override_models,
                logs=logs)
            
            if logs:
                if not result:
                    print('Simulation failed')
                    continue
                
                print(f'Results:')
                for i, name in enumerate(result[:top]):
                    print(f'{i + 1:>3}: {name}')
        
            predictions[event][sex] = result

    return predictions


__all__ = [
    simulate_event,
    simulate_all_events,
]