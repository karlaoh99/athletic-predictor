import sys
import glob
import shutil
import numpy as np
from typing import Callable
from sklearn.metrics import ndcg_score
from src.prediction_saver import load_json, save_json
from src.competition_data import CompetitionData
from src.event_params_optimizer import EventParamsOptimizer


def calculate_error1(result: list, prediction: list) -> int:
    # Adds all the times an athlete is in the actual result 
    # and an athlete is in the exact position
    
    acc = 0
    for i in range(8):
        if prediction[i] in result:
            acc += 1
        if prediction[i] == result[i]:
            acc += 1
    
    return 1 - (acc / 16) 


def calculate_error2(result: list, prediction: list) -> int:
    # Adds the number of positions difference between 
    # the actual result and the predicted one

    e = 0
    for r_index, name in enumerate(result):
        try:
            p_index = prediction.index(name)
            e += abs(r_index - p_index)
        except:
            continue

    return e


def calculate_error3(result: list, prediction: list) -> int:
    # For each athlete adds all the athletes who were above 
    # him in the prediction and not in the real result

    e = 0
    above = []
    for name in result:
        try:
            p_index = prediction.index(name)
            for i in range(0, p_index):
                if prediction[i] not in above:
                    e += 1
            above.append(name)
        except:
            continue

    return e


def calculate_error4(result: list, prediction: list) -> int:
    # Treats the prediction system as an information retrieval system, 
    # maximizing the ndcg_score

    scores = list(range(8, 0, -1)) + [0] * (len(prediction) - 8)
    relevance = []
    for i, name in enumerate(prediction):
        try:
            relevance.append(8 - result.index(name))
        except:
            relevance.append(0)

    relevance = np.asarray([relevance])
    scores = np.asarray([scores])

    return 1 - ndcg_score(relevance, scores)


def _save_config(config: dict, event: str, sex: str, file: str):
    optimal_results = load_json(file)
    
    if not event in optimal_results:
        optimal_results[event] = {}

    if not sex in optimal_results[event]:
        optimal_results[event][sex] = {}
    
    for key, value in config.items():
        optimal_results[event][sex][key] = value

    save_json(optimal_results, file)


def _clean_folders():
    smacList = glob.glob('smac3-output*')
    smacList += ['models']
    for path in smacList:
        shutil.rmtree(path)


def optimize_params(events: list, data: dict, results: dict, competition: CompetitionData, params: list, runcount: int, error_calculator: Callable, file: str):
    
    for event in events:
        for sex in competition.get_event_data(event, 'sex'):
            print(f"Optimizing {event} - {sex}...")
            optimizer = EventParamsOptimizer(
                runcount=runcount,
                calculate_error=error_calculator,
                optimize_params=params,
                default_params={
                    "bandwidth": competition.get_event_param(event, sex, 'bandwidth', 1),
                    "alpha": competition.get_event_param(event, sex, 'alpha', 0),
                    "sim_times": competition.get_event_param(event, sex, 'sim_times', 5000),
                    "pond_times": competition.get_event_param(event, sex, 'pond_times', {str(competition.start_date.year - i) : int(4 / (i+1)) for i in range(3)}),
                }
            )

            optimal_config = optimizer.optimize(data[event][sex], list(results[event][sex].values()), event, sex, competition)
            _save_config(optimal_config, event, sex, file)
            _clean_folders()


__all__ = [
    "calculate_error1",
    "calculate_error2",
    "calculate_error3",
    "calculate_error4",
    "optimize_params",
]