"""
Created on Jan 7, 2014

@author: Matt
"""
import re
#import numpy as np
#import math


class Tab(object):
    """Create python objects for guitar tabs. 

    A 'Tab' object easily facilitates the storage, modification, and textual
    display of a guitar tab in python.
    """

    def __init__(self, clength=6):
        """Constructor"""
        # the maximum length of a line in the tab
        self._MAX = 78
        # the number of strings for a chord, default 6
        self.clength = clength
        # a blank chord
        self._blank = ['-' for x in range(6)]
        # the list that will hold the chords which form the tab
        self.tab_data = [self._blank]
        # string tuning indicator to be printed at the beginning of each tab
        # line
        self._leader = (('e', 'B', 'G', 'D', 'A', 'E'), ('|', '|', '|', '|',
            '|', '|'))
        # allowed entries for a chord list
        self.allowed = ['-', 'h', 'p', 'x'] + [str(x) for x in range(25)]
        # the index for the current position in the tab
        self.i = 0
        # the default name for the file to be written to
        self.file = 'myTab.txt'
        # TODO current place: I think I have finished the __init__ constructor

    def __str__(self):
        """Format Tab.tab_data for printing
        """
        pass

    def write(self, chord, index=None):
        """Writes the input chord to an index of the Tab object

        Parameters
        ----------
        chord : a list of single string characters and of length self.clength
        index : the index of self.tab_data where the chord will be written.
                Default is the current index, self.i

        Returns
        -------
        None
        """

        # Check that the chord has the correct format
        if len(chord) != self._MAX:
            # TODO raise a more informative error here; make my own error
            # class?
            raise TypeError
        for i in chord:
            if i not in self.allowed:
                raise TypeError

        # If the index is unset, then use the default value of the current
        # self.i index
        if index is None:
            index = self.i
        # Otherwise, if the input index is larger than the current index, we
        # need to expand the tab
        else:
            if index > self.i:
                # TODO this logic isn't quite right since it can't be assumed
                # that the current index is at the end of the tab. fix.
                self.tab_data += [self.blank for x in range(index - self.i)]


        # Implement a check for the length of chord?
        self.tab_data[:, self.i] = chord
        print(self)
        self.i += 1
        if self.i >= self._MAX:
            return True
        else:
            return False

    def back(self, num):
        """
        Goes back num places in the tab and places a chord of astericks here.
        Any other astericks chords will be replaced as well.
        """
        if self.i - abs(num) < 2:
            print("Index requested out of bounds; please try again.")
        else:
            for j in range(2, self._MAX - 1):
                if self.tab_data[0, j] == '*':
                    self.tab_data[:, j] = self._blank
            self.i -= abs(num)
            self.tab_data[:, self.i] = self._current
            print(self)

    def forward(self, num):
        if self.i + abs(num) >= self._MAX:
            print("Index requested out of bounds; please try again.")
        else:
            for j in range(2, self._MAX - 1):
                if self.tab_data[0, j] == '*':
                    self.tab_data[:, j] = self._blank
            self.i += abs(num)
            self.tab_data[:, self.i] = self._current
            print(self)

    def open(self, file):
        """
        Open a pyTab file and determine if it should be appended or written
        over.
        """
        # This probably should just be implemented in the main function as a
        # function itself. I should define a file convention.
        pass

    def save(self):
        """
        Write the current tab data to file.
        """
        pass
