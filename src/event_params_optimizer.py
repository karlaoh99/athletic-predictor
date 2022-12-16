import sys
import numpy as np
from typing import List, Callable
from ConfigSpace import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformIntegerHyperparameter, OrdinalHyperparameter, UniformFloatHyperparameter
from smac.facade.smac_hpo_facade import SMAC4HPO
from smac.scenario.scenario import Scenario
from src.ponderator import ponderate_event
from src.simulator import simulate_event
from src.competition_data import CompetitionData


class EventParamsOptimizer:
    def __init__(self, runcount: int, calculate_error: Callable, optimize_params: list, default_params: dict):
        self.runcount = runcount
        self.calculate_error = calculate_error
        self.optimize_params = optimize_params
        self.default_params = default_params
        self.progress = 0

    def optimize(self, x_train: dict, y_train: List[str], event: str, sex: str, competition: CompetitionData):        
        # Define your hyperparameters
        configspace = ConfigurationSpace()
        for param in self.optimize_params:
            configspace.add_hyperparameters(self._get_hyperparameters(param, x_train))
            
        # Provide meta data for the optimization
        scenario = Scenario({
            "run_obj": "quality",   # Optimize quality (alternatively runtime)
            "runcount-limit": self.runcount,   # Max number of function evaluations (the more the better)
            "cs": configspace,
        })

        train = self._get_train(x_train, y_train, event, sex, competition)

        smac = SMAC4HPO(scenario=scenario, tae_runner=train)
        best_found_config = smac.optimize()
        print("Optimization finished    ")
        
        return best_found_config
        
    def _get_train(self, x_train: dict, y_train: List[str], event: str, sex: str, competition: CompetitionData):
        def train(config):
            self.progress += 1
            print(f"Optimizing... {(self.progress * 100 / self.runcount):.2f} %", end="\r")

            bandwidth = self._get_param('bandwidth', config)
            sim_times = int(self._get_param('sim_times', config))
            alpha = self._get_param('alpha', config)

            if 'y0' in config:
                pond_times = {}
                year = competition.start_date.year
                pond_times[str(year-2)] = config['y2']
                pond_times[str(year-1)] = pond_times[str(year-2)] * config['y1']
                pond_times[str(year)] = pond_times[str(year-1)] * config['y0']
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

        return train

    def _get_param(self, param: str, config):
        if param in config:
            return config[param]
        else:
            return self.default_params[param]

    def _get_hyperparameters(self, param: str, x_train) -> list:
        if param == 'bandwidth':
            min = sys.maxsize
            max = 0
            for _, results in x_train.items():
                min = np.min(results.Result.to_list() + [min])
                max = np.max(results.Result.to_list() + [max])
            half_range = (max - min) / 2

            return [
                UniformFloatHyperparameter('bandwidth', lower=1e-3, upper=half_range, log=False)
            ]

        if param == 'sim_times':
            return [
                OrdinalHyperparameter('sim_times', sequence=[str(n) for n in np.arange(5000, 10001, 1000)])
            ]

        if param == 'alpha':
            return [
                UniformFloatHyperparameter('alpha', lower=0, upper=1, log=False)
            ]

        if param == 'pond_times':
            return [
                UniformIntegerHyperparameter('y0', lower=1, upper=5, log=False),
                UniformIntegerHyperparameter('y1', lower=1, upper=5, log=False),
                UniformIntegerHyperparameter('y2', lower=1, upper=5, log=False)
            ]


__all__ = [
    "EventParamsOptimizer",
]