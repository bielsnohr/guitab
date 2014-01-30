'''
Created on Jan 7, 2014

@author: Matt
'''
import re
import numpy as np
import math


class tab(object):
    '''
    Class for the textual display and modification of a guitar tab.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # the maximum length of a tab
        self._MAX = 80
        # the chord indicating the user's current location in the tab
        self._current = ('*', '*', '*', '*', '*', '*')
        # a blank chord
        self._blank = tuple(['-' for x in range(6)])
        # the numpy array that will hold the tab data
        self.tab_data = np.zeros((6, self._MAX), dtype='U2')
        self.tab_data[:, :] = '-'
        self.tab_data[:, 0] = ('e', 'B', 'G', 'D', 'A', 'E')
        self.tab_data[:, 1] = '|'
        # the index for the current column to be written to
        self.i = 2
        # the default name for the file to be written to
        self.file = 'myTab.txt'

    def __str__(self):
        # this convoluted statement formats the numpy array so it looks like a
        # nice tab
        return re.sub('(\[\[)|(\]\])|(\s)|(\')', '',
                      str(self.tab_data)).replace('][', '\n')

    def write(self, chord):
        '''
        Writes the input chord to the current tab. If the tab is full, the
        function returns True, and otherwise it returns False.
        '''
        # Implement a check for the length of chord?
        self.tab_data[:, self.i] = chord
        print(self)
        self.i += 1
        if self.i >= self._MAX:
            return True
        else:
            return False

    def back(self, num):
        '''
        Goes back num places in the tab and places a chord of astericks here.
        Any other astericks chords will be replaces as well.
        '''
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
        '''
        Open a pyTab file and determine if it should be appended or written
        over.
        '''
        # This probably should just be implemented in the main function as a
        # function itself. I should define a file convention.
        pass

    def save(self):
        '''
        Write the current tab data to file.
        '''
        pass
