"""Format Tab objects for output to file"""
from abc import ABC, abstractmethod
from copy import copy
from pathlib import Path
from typing import Dict, List, IO, AnyStr, Union


Pathish = Union[AnyStr, Path]  # in lieu of yet-unimplemented PEP 519
FileSpec = Union[IO, Pathish]


class TabFormatter(ABC):
    """Abstract base class that defines the interface for formatting Tab objects
    """

    def __init__(self) -> None:
        self._tab_metadata = {k: '' for k in ('author', 'date', 'title', 'tuning')}
        self._tab_data = []

    def set_metadata(self, author: str, date: str, title: str, tuning: List[str], **kwargs) -> None:
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
        self._tab_data = copy(data)

    def get_data(self) -> List[List[str]]:
        """Get the Tab data currently stored in the Formatter object

        Returns
        -------
        List[List[str]]
            The tab data as a Tab object understands it. See :py:meth:`set_data`
            for description of this data.
        """
        # TODO should there be validation of the internal data here? Or perhaps
        # at the point it is set in the Formatter object?
        return copy(self._tab_data)

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


class TxtTabFormatter(TabFormatter):
    """Class for formatting a tab to a text file."""

    DEFAULT_LINE_LENGTH = 78
    BREAK_LINE = 80 * '='

    @classmethod
    def convert_tab_to_string(cls, tab_data: List[List[AnyStr]],
                              tuning: List[AnyStr],
                              index: int = None,
                              line_length: int = DEFAULT_LINE_LENGTH) -> AnyStr:
        """Convert a Tab object's tab data (not metadata) into a string representation

        Parameters
        ----------
        tab_data : List[List[AnyStr]]
            The Tab object's tab data
        tuning : List[AnyStr]
            The tuning to be used for the guitar
        index : int, optional
            The current writing position in the tab, by default None. If
            present, an asterix ('*') will be placed under one of the tab bars
            where this current position is.
        line_length : int, optional
            The width of the line at which the tab should be wrapped, by default DEFAULT_LINE_LENGTH

        Returns
        -------
        AnyStr
            The string representation of the tab data
        """
        number_of_loops = ((len(tab_data) - 1) // line_length) + 1
        if index is not None:
            loop_position = index // line_length
        tab_string = ''
        chord_length = len(tab_data[0])

        # loop through the rows of tabs that will be created by breaking them
        # into suitable line lengths
        for i in range(number_of_loops):

            start = i * line_length
            if i == number_of_loops - 1:
                end = len(tab_data)
            else:
                end = start + line_length

            for j in range(chord_length):

                tab_string = tab_string + tuning[j] + '|'
                for k in range(start, end):
                    tab_string = tab_string + tab_data[k][j]
                tab_string = tab_string + '\n'

            if index is not None and i == loop_position:
                pad = index - start + 2
                tab_string = tab_string + ' ' * pad + '*'

            if i == number_of_loops - 1:
                tab_string = tab_string + '\n'
            else:
                tab_string = tab_string + '\n\n'

        return tab_string

    def _write_formatted_tab(self, fileobj: IO) -> None:
        """Write the tab data formatted as a UTF-8 text file

        Parameters
        ----------
        fileobj : IO
            The text file object to which the tab will be written
        """
        tab_str = TxtTabFormatter.convert_tab_to_string(
            tab_data=self._tab_data, tuning=self._tab_metadata['tuning'])
        file_text = \
            TxtTabFormatter.BREAK_LINE + '\n' + \
            'Title : {title}\n' + \
            'Author: {author}\n' + \
            'Date  : {date}\n' + \
            TxtTabFormatter.BREAK_LINE + '\n\n' + \
            '{tabdata}'
        fileobj.write(file_text.format(tabdata=tab_str, **self._tab_metadata))
