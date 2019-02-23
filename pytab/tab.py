"""
Created on Jan 7, 2014

@author: Matt
"""
#import re
#import numpy as np
#import math


class Tab(object):
    """Create python objects for guitar tabs. 

    A 'Tab' object easily facilitates the storage, modification, and textual
    display of a guitar tab in python.
    """

    def __init__(self, clength=6):
        """Constructor for Tab class object"""
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
        # the current size of the tab (i.e. largest index attained so far)
        self.imax = 0
        # the default name for the file to be written to
        self.file = 'myTab.txt'


    def __str__(self):
        """Format Tab.tab_data for printing
        """
        
        num_loops = (self.imax // self._MAX) + 1
        pos_loop = self.i // self._MAX
        tab_string = ''

        # loop through the rows of tabs that will be created by breaking them
        # into suitable line lengths
        for i in range(num_loops):

            #import pdb; pdb.set_trace()
            start = i * self._MAX
            if i == num_loops - 1:
                end = self.imax + 1
            else:
                end = start + self._MAX

            for j in range(self.clength):

                for k in range(start, end):
                    tab_string = tab_string + self.tab_data[k][j]

                tab_string = tab_string + '\n'

        return tab_string



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
        if len(chord) != self.clength:
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
        # Otherwise, if the input index is larger than the maximum index,
        # self.imax, we need to expand the tab
        else:
            if index > self.imax:
                self.tab_data += [self._blank for x in range(index - self.imax)]
                self.imax = index

        # Add the chord to the tab data and print what we have
        self.tab_data[index] = chord
        #print(self)

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
