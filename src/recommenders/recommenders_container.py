from src.recommenders.factory import *
from src.shared.container import Container
from src.shared.generic_factory import GenericFactory

class RecommendersContainer(Container):
    """

    """

    def __init__(self, parameters: dict) -> None:
        """
        @type stages: list

        """

        super().__init__()
        recommenders = parameters['instances']

        if len(recommenders) == 0:
            pass
        else:
            self.recommender_factory = GenericFactory(parameters)
            self.insert(0, self.recommender_factory.create)