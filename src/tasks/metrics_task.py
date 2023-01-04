import pandas as pd
import os
from src.tasks.task import Task
from src.experiments.experiment_handler import ExperimentHandler
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path
from lenskit import topn
from src.metrics.cross_validation import CrossValidation
class MetricsTask(Task):
    def __init__(self, metrics, args = None):
        """

        @param args:
        """

        self.cross_validation = CrossValidation({
            'lib': '',
            'metrics': '',
            'X': '',
            'y': '',
            'cv': '',
            'return_train_score': '',
            'return_estimator': '',
            'error_score': ''
        })
        self.metric_instances = metrics


        self.predictions_output_path = hrf_experiment_output_path().joinpath(
            "models/results/predictions/"
        )
        self.evaluate_output_path = hrf_experiment_output_path().joinpath(
            "evaluate/"
        )
        self.experiment_output_dir = hrf_experiment_output_path()
        self.preprocessing_output_dir = self.experiment_output_dir.joinpath("preprocessing/")
        self.algorithms_output_dir = self.experiment_output_dir.joinpath("models/results/")
        self.predictions_output_dir = self.algorithms_output_dir.joinpath("predictions/")
        self.rankings_output_dir = self.algorithms_output_dir.joinpath("rankings/")
        self.recommendations_output_dir = self.algorithms_output_dir.joinpath("recommendations/")

    def check_args(self, args):
        """

        @param args:
        @return:
        """
        pass

    def run(self):
        """

        @return:
        """
        metrics = self.handle_metrics_tasks(self.metric_instances)
        return metrics


    def get_truth_data_file_names(self):
        """
        Vai buscar todos os arquivos de validação (folds) e usa-los para testar as
        predições

        @return:
        """
        validation_folds_dir = self.preprocessing_output_dir.joinpath("folds/validation/")
        file_names = []
        for path in os.scandir(validation_folds_dir):
            if path.is_file():
                file_names.append(path.name)


        return file_names
    def get_results_file_names(self, result_type: str) -> list:
        if result_type not in ['recommendations', 'predictions', 'rankings']:
            raise Exception("O valor de fold_type está invalido, tente: train ou validation")

        folds_directory = self.algorithms_output_dir.joinpath("{}.csv".format(result_type))
        file_names = []
        for path in os.scandir(folds_directory):
            if path.is_file():
                file_names.append(path.name)

        return file_names

    def topn_evaluation(self, metrics: list, recommendations: pd.DataFrame,  dataset_test: pd.DataFrame) -> pd.DataFrame:
        print("topn_evaluation")
        topn_metrics = {
            'ndcg': topn.ndcg,
            'dcg': topn.dcg,
            'precision': topn.precision,
            'recall': topn.recall,
            'hit': topn.hit
        }

        all_recs = recommendations
        test_data = dataset_test

        topn_analysis = topn.RecListAnalysis()
        for metric in metrics:
            m = topn_metrics[metric]
            topn_analysis.add_metric(m)

        results = topn_analysis.compute(all_recs, test_data)
        print("topn analysis result: ", results)
        return results



    def handle_metrics_tasks(self, metrics):
        rec_files = self.get_results_file_names('recommendations')
        pred_files = self.get_results_file_names('predictions')
        ranking_files = self.get_results_file_names('rankings')
        truth_files = self.get_truth_data_file_names()
        results_files = zip(pred_files, rec_files, ranking_files, truth_files)

        for pred, rec, rank, truth_files in results_files:
            print("prediction path: ", pred)
            print("recommendation path: ", rec)
            print("ranking path: ", rank)
            print("truth files: ", truth_files)

            prediction = pd.read_csv(pred)
            recommendation = pd.read_csv(rec)
            ranking = pd.read_csv(rank)
            validation = pd.read_csv(ranking)

            self.topn_evaluation(
                metrics,
                recommendation,
                validation
            )

            cv_result = self.cross_validation.evaluation_sklearn()
            print("cross validation result")
            print(cv_result)



        return metrics



def run_metrics_task():
    loader = Loader()
    config_obj = loader.load_json_file("config.json")

    experiments = config_obj['experiments']
    exp_handler = ExperimentHandler(
        experiments=experiments
    )
    experiment = exp_handler.get_experiment("exp1")
    experiment_instances = experiment.instances

    metrics_instance = experiment_instances['metrics']

    metrics_task = MetricsTask(metrics_instance)

    print(" => Iniciando tarefa de cálculo das métricas")
    print(" => Finalizando tarefa de cálculo das métricas")

    metrics_task.run()


run_metrics_task()