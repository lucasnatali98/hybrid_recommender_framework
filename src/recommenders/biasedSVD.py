from src.recommenders.recommender import Recommender
from src.utils import process_parameters
from pandas import DataFrame, Series, concat
from lenskit.algorithms.als import BiasedMF
from lenskit.algorithms import Recommender as LenskitRecommender


class BiasedSVD(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = {
            'iterations',
            'features'
        }

        parameters = process_parameters(parameters, default_keys)

        self.features = parameters['features']
        self.damping = parameters['damping']
        self.BiasedMF = BiasedMF(
            features=self.features,
            iterations=20
        )
        self.BiasedMF = LenskitRecommender.adapt(self.BiasedMF)

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """

        return self.BiasedMF.predict_for_user(user,items,ratings)

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        return self.BiasedMF.predict(pairs, ratings)

    def recommend(self, users, n, candidates=None, ratings=None):
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        recommendation_dataframe = DataFrame(
            columns=['user', 'item', 'score', 'algorithm_name']
        )
        for user in users:
            recommendation_to_user = self.PopScore.recommend(user, n)

            names = Series([self.__class__.__name__] * n)
            user_id_list = Series([user] * n)

            recommendation_to_user['algorithm_name'] = names
            recommendation_to_user['user'] = user_id_list

            recommendation_dataframe = concat(
                [recommendation_dataframe, recommendation_to_user],
                ignore_index=True
            )

        return recommendation_dataframe

    def get_params(self, deep=True):
        """

        @param deep:
        @return:
        """
        pass

    def fit(self, rating, **kwargs):
        """

        @param rating:
        @param kwargs:
        @return:
        """
        self.BiasedMF.fit(rating)
