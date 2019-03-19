"""
Created on Jan 7, 2014

@author: Matt
"""

import datetime as dt
import warnings


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
        self._leader = ('e|', 'B|', 'G|', 'D|', 'A|', 'E|')

        # allowed entries for a chord list
        self.allowed = ['-', 'h', 'p', 'x'] + [str(x) for x in range(25)]

        # the index for the current position in the tab
        self.i = 0
        
        # the current size of the tab (i.e. largest index attained so far)
        self.imax = 0

        # the dictionary that holds the information about the tab; defaults set
        today = str(dt.date.today())
        self.info = {'filename':'myTab.txt', 'title':'My Tab', 'author':'Me', 
                'date':today} 


    def __str__(self):
        """Format Tab.tab_data for printing
        """
        
        num_loops = (self.imax // self._MAX) + 1
        pos_loop = self.i // self._MAX
        tab_string = ''

        # loop through the rows of tabs that will be created by breaking them
        # into suitable line lengths
        for i in range(num_loops):

            start = i * self._MAX
            if i == num_loops - 1:
                end = self.imax + 1
            else:
                end = start + self._MAX

            for j in range(self.clength):

                tab_string = tab_string + self._leader[j]
                for k in range(start, end):
                    tab_string = tab_string + self.tab_data[k][j]
                tab_string = tab_string + '\n'

            if i == pos_loop:
                pad = self.i - start + 2
                tab_string = tab_string + ' ' * pad + '*'

            if i == num_loops - 1:
                tab_string = tab_string + '\n'
            else:
                tab_string = tab_string + '\n\n'

        return tab_string


    def print(self):
        """Format Tab.tab_data for limited printing. This routine prints the
        tab object with the same formatting as calling `print(tab_instance)`
        but only three tab rows are printed: the row that the current chord
        position falls in and the two encapsulating rows (i.e. preceding and
        following rows).
        """
        
        num_loops = (self.imax // self._MAX)
        pos_loop = self.i // self._MAX
        tab_string = ''

        start_out = pos_loop - 1
        end_out = pos_loop + 2

        # TODO amend this so that it always prints 3 rows if they are
        # available
        if pos_loop == 0:
            start_out = 0
        if pos_loop == num_loops:
            end_out = num_loops + 1

        # loop through the rows of tabs that will be created by breaking them
        # into suitable line lengths
        for i in range(start_out, end_out):

            start = i * self._MAX
            if i == end_out - 1:
                end = self.imax + 1
            else:
                end = start + self._MAX

            for j in range(self.clength):

                tab_string = tab_string + self._leader[j]
                for k in range(start, end):
                    tab_string = tab_string + self.tab_data[k][j]
                tab_string = tab_string + '\n'

            if i == pos_loop:
                pad = self.i - start + 2
                tab_string = tab_string + ' ' * pad + '*'

            if i == end_out - 1:
                tab_string = tab_string + '\n'
            else:
                tab_string = tab_string + '\n\n'

        print(tab_string)


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
        # TODO I need to handle double digit fret numbers!!!

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
        # TODO need to check that the index is positive and an integer!!!
        else:
            if index > self.imax:
                self.tab_data += [self._blank for x in range(index - self.imax)]
                self.imax = index

        # Add the chord to the tab data and print what we have
        self.tab_data[index] = chord
        self.print()


    def backward(self, num=1):
        """Place the chord position back `num` places from where it currently
        is.


        Parameters
        ----------
        num   : The number of places to go backwards in the tab. Must be an
                integer > 0. Default is 1.

        Returns
        -------
        None
        """

        if num < 0 or type(num) != int:
            raise TypeError('num argument must be an integer and > 0. num = '\
                    '{}'.format(num))

        elif self.i - num < 0:
            raise IndexError('Requested backwards move is out of range. Index'\
                    '= {:d}, and num = {:d}'.format(self.i, num))

        else:
            self.i -= num
            self.print()


    def forward(self, num=1):
        """Place the chord position forward `num` places from where it
        currently is.


        Parameters
        ----------
        num   : The number of places to go forward in the tab. Must be an
                integer > 0. Default is 1.

        Returns
        -------
        None
        """

        if num < 0 or type(num) != int:
            raise TypeError('num argument must be an integer and > 0. num = '\
                    '{}'.format(num))

        # We can add to the present index without restriction as long as the
        # above is satisfied
        self.i += num

        # Check if the new index is greater than the previous maximum. If so,
        # the tab needs to be expanded
        if self.i > self.imax:
            self.tab_data += [self._blank for x in range(self.i - self.imax)]
            self.imax = self.i

        self.print()


    def set_info(self, **kwargs):
        """Set relevant information for the Tab object, such as author, date,
        etc. 
        
        Keyword arguments accepted
        ---
        filename : the name of the file to which the tab should be read/written
                   (str)
        title    : the title of the tab (str)
        author   : the author of the tab (str)
        date     : the date the tab was written (str)

        """

        for i in kwargs:

            if not self.info.__contains__(i):
                message = 'The field requested, "{}", is not valid for tab '\
                        'info.'.format(i)
                warnings.warn(message)
                continue
            else:
                if type(kwargs[i]) is not str:
                    message = 'The input for field, "{}", is not of type '\
                            'str. All tab information must be str.'.format(i)
                    warnings.warn(message)
                else:
                    self.info[i] = kwargs[i]



    def get_tab(self, filename):
        """
        Open a pyTab file and determine if it should be appended or written
        over.


        Parameters
        ----------
        num   : The number of places to go forward in the tab. Must be an
                integer > 0. Default is 1.

        Returns
        -------
        None
        """
        pass


    def save_tab(self, filename=None, **kwargs):
        """
        Write the current tab data to file.


        Parameters
        ----------
        filename : The name of the file to write to

        Keyword arguments accepted
        ---
        filename : the name of the file to which the tab should be read/written
                   (str)
        title    : the title of the tab (str)
        author   : the author of the tab (str)
        date     : the date the tab was written (str)

        Returns
        -------
        None
        """

        if filename is None:
            self.set_info(**kwargs)
        else:
            self.set_info(filename=filename, **kwargs)


