"""Format Tab objects for output to file"""
from abc import ABC, abstractmethod
from os import PathLike
from typing import Dict, List


class TabFormatter(ABC):
    """Abstract base class that defines the interface for formatting Tab objects
    """

    def set_metadata(self, author: str, date: str, title: str) -> None:
        pass

    def get_metadata(self) -> Dict[str, str]:
        pass

    def set_data(self, data: List[List[str]]) -> None:
        pass

    def get_data(self) -> List[List[str]]:
        pass

    @abstractmethod
    def save(self, file: PathLike) -> None:
        pass

    @abstractmethod
    def load(self, file: PathLike) -> None:
        pass
