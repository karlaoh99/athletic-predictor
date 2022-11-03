import sys
import numpy as np
from typing import List, Callable
from ConfigSpace import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformIntegerHyperparameter, OrdinalHyperparameter
from smac.facade.smac_bb_facade import SMAC4BB
from smac.scenario.scenario import Scenario
from src.simulator import simulate_event
from src.competition_data import CompetitionData
from src.ponderator import ponderate_event
from src.simulator import simulate_event


class EventOptimizer:
    def __init__(self, runcount: int, calculate_error: Callable, optimize_params: list, default_params: dict):
        self.runcount = runcount
        self.calculate_error = calculate_error
        self.optimize_params = optimize_params
        self.default_params = default_params

    def optimize(self, x_train: dict, y_train: List[str], event: str, sex: str, competition: CompetitionData):        
        # Define your hyperparameters
        configspace = ConfigurationSpace()

        for param in self.optimize_params:
            configspace.add_hyperparameters(self.get_hyperparameters(param, x_train))
            
        # Provide meta data for the optimization
        scenario = Scenario({
            "run_obj": "quality",   # Optimize quality (alternatively runtime)
            "runcount-limit": self.runcount,   # Max number of function evaluations (the more the better)
            "cs": configspace,
        })

        train_kde = self._get_train_kde(x_train, y_train, event, sex, competition)

        smac = SMAC4BB(scenario=scenario, tae_runner=train_kde)
        best_found_config = smac.optimize()
        
        return best_found_config
        
    def _get_train_kde(self, x_train: dict, y_train: List[str], event: str, sex: str, competition: CompetitionData):
        def train_kde(config):
            bandwidth = self._get_param('bandwidth', config)
            sim_times = int(self._get_param('sim_times', config))
            alpha = self._get_param('alpha', config)
            
            if 'y0' in config:
                pond_times = {}
                year = competition.start_date.year
                pond_times[year] = config['y0']
                pond_times[year-1] = config['y1']
                pond_times[year-2] = config['y2']

                if config['y0'] < config['y1'] or config['y1'] < config['y2']:
                    return 10000

            else:
                pond_times = self.default_params['pond_times']

            competition.set_event_param(event, sex, 'bandwidth', bandwidth)
            competition.set_event_param(event, sex, 'sim_times', sim_times)

            pond_data = ponderate_event(
                data=x_train, 
                maximize=competition.is_maximize_event(event), 
                years_weight=pond_times,
                alpha=alpha
            )

            sim_result = simulate_event(
                data=pond_data, 
                event=event, 
                sex=sex,
                competition=competition,
                times=sim_times,
                models_folder='models',
                override_models=True, 
            )

            return self.calculate_error(y_train, sim_result)    

        return train_kde

    def _get_param(self, param: str, config):
        if param in config:
            return config[param]
        else:
            return self.default_params[param]

    def get_hyperparameters(self, param: str, x_train) -> list:
        if param == 'bandwidth':
            min = sys.maxsize
            max = 0
            for _, results in x_train.items():
                min = np.min(results.Result.to_list() + [min])
                max = np.max(results.Result.to_list() + [max])
            half_range = (max - min) / 2

            return [
                OrdinalHyperparameter('bandwidth', sequence=np.linspace(1e-3, half_range, self.runcount))
            ]

        if param == 'sim_times':
            return [
                OrdinalHyperparameter('sim_times', sequence=[str(n) for n in np.arange(1000, 10001, 1000)])
            ]

        if param == 'alpha':
            return [
                OrdinalHyperparameter('alpha', sequence=np.linspace(0, 0.99, self.runcount))
            ]

        if param == 'pond_times':
            return [
                UniformIntegerHyperparameter('y0', lower=1, upper=8, log=False),
                UniformIntegerHyperparameter('y1', lower=1, upper=8, log=False),
                UniformIntegerHyperparameter('y2', lower=1, upper=8, log=False)
            ]


class PondYearsOptimizer:
    def __init__(self, runcount: int, calculate_error: Callable):
        self.runcount = runcount
        self.calculate_error = calculate_error

    def optimize(self, x_train: dict, y_train: List[str], competition: CompetitionData):        
        # Define your hyperparameters
        configspace = ConfigurationSpace()

        configspace.add_hyperparameter(UniformIntegerHyperparameter('y0', lower=1, upper=8, log=False))
        configspace.add_hyperparameter(UniformIntegerHyperparameter('y1', lower=1, upper=8, log=False))
        configspace.add_hyperparameter(UniformIntegerHyperparameter('y2', lower=1, upper=8, log=False))

        # Provide meta data for the optimization
        scenario = Scenario({
            "run_obj": "quality",   # Optimize quality (alternatively runtime)
            "runcount-limit": self.runcount,   # Max number of function evaluations (the more the better)
            "cs": configspace,
        })

        train_kde = self._get_train_kde(x_train, y_train, competition)

        smac = SMAC4BB(scenario=scenario, tae_runner=train_kde)
        best_found_config = smac.optimize()
        
        return best_found_config
        
    def _get_train_kde(self, x_train: dict, y_train: List[str], competition: CompetitionData):
        def train_kde(config):
            
            pond_times = {}
            year = competition.start_date.year
            pond_times[year] = config['y0']
            pond_times[year-1] = config['y1']
            pond_times[year-2] = config['y2']

            if config['y0'] < config['y1'] or config['y1'] < config['y2']:
                return 10000

            print(pond_times)
            
            error = 0
            for event in competition.events:
                for sex in competition.get_event_data(event, 'sex'):
                    x = x_train[event][sex]
                    y = list(y_train[event][sex].values())

                    pond_data = ponderate_event(
                        data=x, 
                        maximize=competition.is_maximize_event(event), 
                        years_weight=pond_times,
                        alpha=competition.get_event_param(event, sex, 'alpha', 0)
                    )

                    sim_result = simulate_event(
                        data=pond_data, 
                        event=event, 
                        sex=sex,
                        competition=competition,
                        times=1000,
                        models_folder='models',
                        override_models=True, 
                    )

                    error += self.calculate_error(y, sim_result) 

            return error    

        return train_kde


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


__all__ = [
    "EventOptimizer",
    "PondYearsOptimizer",
    "calculate_error1",
    "calculate_error2",
    "calculate_error3",
]