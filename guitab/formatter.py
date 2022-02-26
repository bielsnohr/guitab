"""Format Tab objects for output to file"""
from abc import ABC, abstractmethod
from os import PathLike
from typing import Dict, List
from .tab import Tab


class TabFormatter(ABC):
    """Abstract base class that defines the interface for formatting Tab objects
    """

    def __init__(self) -> None:
        self._tab_metadata = {k: '' for k in ('author', 'date', 'title', 'tuning')}
        self._tab_data = []

    def set_metadata(self, author: str, date: str, title: str, tuning: List[str] = Tab.DEFAULT_TUNING) -> None:
        """Set the metadata for a tab in the TabFormatter object

        Parameters
        ----------
        author : str
            The name of the author of the tab
        date : str
            The date the tab was created or updated
        title : str
            The title of the tab
        tuning : List[str], optional
            The guitar tuning specified by the tab, where each chord is given a
            note that it is set to, by default Tab.DEFAULT_TUNING
        """
        # This will be improved with data class to hold metadata
        self._tab_metadata['author'] = author
        self._tab_metadata['date'] = date
        self._tab_metadata['title'] = title
        self._tab_metadata['tuning'] = tuning

    def set_data(self, data: List[List[str]]) -> None:
        """Set the Tab data to be formatted in the Formatter

        Parameters
        ----------
        data : List[List[str]]
            The Tab data to be formatted. This input data is held in the same
            manner as the internal Tab class holds it: the top level list holds
            all of the chords that make up the tab, each element is a list of
            strings that represents one of those chords, with each string one of
            the finger positions for each guitar string.
        """
        # TODO would probably be better to create a copy of the data because this is a mutable type
        self._tab_data = data

    @abstractmethod
    def save(self, file: PathLike) -> None:
        pass

    @abstractmethod
    def load(self, file: PathLike) -> None:
        pass
