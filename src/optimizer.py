from ConfigSpace import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformFloatHyperparameter, UniformIntegerHyperparameter, OrdinalHyperparameter
from smac.facade.smac_bb_facade import SMAC4BB
from smac.scenario.scenario import Scenario

from sklearn.neighbors import KernelDensity
from datetime import date
from ponderator import ponderate_marks
   

class SMAC4BBOptimizer:
    def __init__(self, runcount):
        self.runcount = runcount

    def optimize(self, x_train, y_train, maximize):
        # Define your hyperparameters
        configspace = ConfigurationSpace()
        configspace.add_hyperparameter(UniformFloatHyperparameter('bandwidth', lower=0.1, upper=5, log=False))
        configspace.add_hyperparameter(UniformIntegerHyperparameter('n_years', lower=2, upper=5, log=False))
        configspace.add_hyperparameter(OrdinalHyperparameter('n_sim', sequence=[str(n) for n in np.arange(500, 5001, 500)]))

        # Provide meta data for the optimization
        scenario = Scenario({
            "run_obj": "quality",   # Optimize quality (alternatively runtime)
            "runcount-limit": self.runcount,   # Max number of function evaluations (the more the better)
            "cs": configspace,
        })

        train_kde = self._get_train_kde(x_train, y_train, maximize)

        smac = SMAC4BB(scenario=scenario, tae_runner=train_kde)
        best_found_config = smac.optimize()
        
        return best_found_config

    def _get_train_kde(self, x_train, y_train, maximize):
        def train_kde(config):
            pond_times = {}
            year = date.today().year
            for i in range(config['n_years'], -1, -1):
                pond_times[year - i] = 2**(config['n_years']-i)

            error = 0
            for x, y in zip(x_train, y_train):
                pond_x = ponderate_marks(x, maximize, pond_times)
                model = KernelDensity(bandwidth=config['bandwidth'], kernel='gaussian')
                model.fit(X = pond_x.Result.to_numpy().reshape((-1,1)))
                
                samples = model.sample(int(config['n_sim']))
                ave = sum([s[0] for s in samples]) / len(samples)
                error += abs(y - ave)

            return error 

        return train_kde


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