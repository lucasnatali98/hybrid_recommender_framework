from abc import abstractmethod
from src.recommenders.recommender import Recommender
from src.utils import is_structure_empty
import importlib
from typing import TypeVar, Generic, List, Dict, Type
from src.shared.generic_factory import AbstractEntityFactory

T = TypeVar('T')

class RecommenderFactory(AbstractEntityFactory[T]):
    """

    """
    def __init__(self, parameters: dict) -> None:
        self.parameters = self._handle_config_obj(parameters)

    def _handle_config_obj(self, parameters: dict) -> dict:
        """
        Tem como objetivo verificar a validade do arquivo de configuração para a execução
        das etapas de pré-processamento

        @type parameters: object
        @param config_obj:
        @return: object or None
        """

        recommenders = parameters['instances']
        is_empty = is_structure_empty(recommenders)

        if is_empty:
            raise Exception("Não foram inseridos estágios de pré-processamento, esse array não deve estar vazio")

        return parameters



    @property
    def create(self) -> List[T]:
        """
        Cria uma instância de um objeto do tipo PreProcessing

        @return: object
        """
        instances = []
        for stages in self.parameters['instances']:
            class_module = stages['module']
            class_name = stages['class_name']

            module = importlib.import_module(class_module)
            class_ = getattr(module, class_name)

            instance = class_(stages['parameters'])
            instances.append(instance)

        return instances