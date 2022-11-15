from src.experiments.experiment import AbstractExperiment, Experiment
from src.shared.container import Container
from typing import List

class ExperimentHandler(Container):
    def __init__(self, experiments, experiment_dependencies: dict = None) -> None:
        """

        """
        super().__init__()

        experiment = Experiment(experiments[0])
        self.items.append(experiment)
    def run_experiments(self) -> dict:
        result = {}
        print("Quantidade de experimentos que serão executados: ", len(self.items))
        for experiment in self.items:
            result[experiment.experiment_id] = experiment.run()

        return result

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass
