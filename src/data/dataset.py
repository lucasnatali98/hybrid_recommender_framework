from abc import ABC, abstractmethod
from src.data.loader import Loader


class Dataset(ABC):
    """
    
    
    """

    @abstractmethod
    def ratings(self):
        """
        
        """
        pass

    @abstractmethod
    def users(self):
        """
        
        """
        pass

    @abstractmethod
    def items(self):
        """
        
        """
        pass


class AbstractDataSet(Dataset):
    """
        
    """

    def __init__(self, items=None, ratings=None, links=None, tags=None):
        """

        @param items:
        @param ratings:
        @param links:
        @param tags:
        """

        self.Loader = Loader()





    def ratings(self):
        """

        @return:
        """
        return self.ratings


    def users(self):
        """

        @return:
        """
        return self.users


    def items(self):
        """

        @return:
        """
        return self.items


