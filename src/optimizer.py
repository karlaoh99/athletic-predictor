from ConfigSpace import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformFloatHyperparameter, UniformIntegerHyperparameter, OrdinalHyperparameter
from smac.facade.smac_bb_facade import SMAC4BB
from smac.scenario.scenario import Scenario

from typing import List, Callable
import numpy as np

from src.simulator import simulate_event
from src.competition_data import CompetitionData
from src.ponderator import ponderate_event
from src.simulator import simulate_event


class SMAC4BBOptimizer:
    def __init__(self, runcount: int, calculate_error: Callable):
        self.runcount = runcount
        self.calculate_error = calculate_error

    def optimize(self, x_train: dict, y_train: List[str], event: str, sex: str, competition: CompetitionData):        
        # Define your hyperparameters
        configspace = ConfigurationSpace()

        # Hyperparameter Bandwidth
        min = 5000
        max = 0
        for _, results in x_train.items():
            min = np.min(results.Result.to_list() + [min])
            max = np.max(results.Result.to_list() + [max])
        half_range = (max - min) / 2

        configspace.add_hyperparameter(OrdinalHyperparameter('bandwidth', sequence=np.linspace(1e-3, half_range, self.runcount)))

        # Hyperparameter Number of Simulations
        # configspace.add_hyperparameter(OrdinalHyperparameter('n_sim', sequence=[str(n) for n in np.arange(500, 5001, 500)]))

        # configspace.add_hyperparameter(UniformIntegerHyperparameter('n_years', lower=2, upper=5, log=False))
        # configspace.add_hyperparameter(UniformIntegerHyperparameter('y0', lower=1, upper=8, log=False))
        # configspace.add_hyperparameter(UniformIntegerHyperparameter('y1', lower=1, upper=8, log=False))
        # configspace.add_hyperparameter(UniformIntegerHyperparameter('y2', lower=1, upper=8, log=False))

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
            # pond_times = {}
            # year = date.today().year
            # # for i in range(config['n_years'], -1, -1):
            # #     pond_times[year - i] = 2**(config['n_years']-i)
            # pond_times[year] = config['y0']
            # pond_times[year-1] = config['y1']
            # pond_times[year-2] = config['y2']
            
            competition.set_event_param(event, sex, 'bw', config['bandwidth'])
            competition.set_event_param(event, sex, 'sim_times', 1000)

            pond_times = {
            2022: 4,
            2021: 2,
            2020: 1,
            }
            
            pond_data = ponderate_event(
                data=x_train, 
                maximize=competition.is_maximize_event(event), 
                years_weight=pond_times,
                alpha=0
            )

            sim_result = simulate_event(
                data=pond_data, 
                event=event, 
                sex=sex,
                competition=competition,
                times= 1000,
                models_folder='models',
                override_models=True, 
            )

            return self.calculate_error(y_train, sim_result)    

        return train_kde


def calculate_error1(result, prediction):
    acc = 0
    for i in range(8):
        if prediction[i] in result:
            acc += 1
        if prediction[i] == result[i]:
            acc += 1
    
    return 1 - (acc / 16) 


def calculate_error2(result, prediction):
    e = 0
    for r_index, name in enumerate(result):
        try:
            p_index = prediction.index(name)
            e += abs(r_index - p_index)
        except:
            continue

    return e


def calculate_error3(result, prediction):
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


def create_dataset(data: dict):
    # Takes the last result obtain for each athlete to y_train and the rest to x_train
    
    x_train = {}
    y_train = {}
    for event in data:
        x_train[event] = {}
        y_train[event] = {}
        
        for sex in data[event]:
            x_train[event][sex] = []
            y_train[event][sex] = []

            for _, df in data[event][sex].items():
                marks = df.Result.array 

                # If the athlete have less than 2 results it is not taken in account to the dataset
                if len(marks) > 1:
                    x_train[event][sex].append(df.iloc[1:])
                    y_train[event][sex].append(df.iloc[0].Result)
    
    return x_train, y_train