"""Format Tab objects for output to file"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, IO, AnyStr, Union
from .tab import Tab


Pathish = Union[AnyStr, Path]  # in lieu of yet-unimplemented PEP 519
FileSpec = Union[IO, Pathish]


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

    def get_metadata(self) -> Dict[str, str]:
        pass

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

    def get_data(self) -> List[List[str]]:
        pass

    def save(self, fileobj: FileSpec) -> None:
        """Save the formatted tab to a file object

        This is the public method that should be used for saving tabs since it
        accepts both string-like and file-like inputs.

        Parameters
        ----------
        fileobj : Union[AnyStr, Path, IO]
            The file (either the open actual file object or string path) to
            which to write the formatted tab.
        """
        if isinstance(fileobj, (str, bytes, Path)):
            with open(fileobj, 'w') as f:
                self._write_formatted_tab(f)
        else:
            self._write_formatted_tab(fileobj)

    def load(self, fileobj: FileSpec) -> None:
        pass

    @abstractmethod
    def _write_formatted_tab(self, fileobj: IO) -> None:
        pass
