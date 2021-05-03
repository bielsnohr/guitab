"""A module for representing guitar tablature
"""

import datetime as dt
import warnings
import re


"""Compiled regex search to remove position cursor in tab"""
rm_position = re.compile(r'(^\s+)\*(\s*$)', flags=re.MULTILINE)
"""Compiled regex search to find title field in tab text file"""
title = re.compile(r'^title\s*:\s*(.*)\s*$', flags=re.IGNORECASE)
"""Compiled regex search to find author field in tab text file"""
author = re.compile(r'^author\s*:\s*(.*)\s*$', flags=re.IGNORECASE)
"""Compiled regex search to find date field in tab text file"""
date = re.compile(r'^date\s*:\s*(.*)\s*$', flags=re.IGNORECASE)

info_tests = {'title': title, 'author': author, 'date': date}
"""Define the order for reading metadata from a tab file"""
info_order = ['title', 'author', 'date']


class Tab(object):
    """Class to represent textual guitar tabs.

    A 'Tab' object easily facilitates the storage, modification, and textual
    display of a guitar tab in Python.
    """

    def __init__(self, clength=6):
        """Constructor for Tab class object


        Parameters
        ----------
        clength : int, optional
            The "length" of a chord, i.e. the number of strings of the guitar.
            The default is 6 which corresponds to the usual 6-string guitar.
            WIP not yet implemented
        """

        # the maximum length of a line in the tab
        self._MAX = 78

        # the number of strings for a chord, default 6
        self.clength = clength

        # a blank chord
        self._blank = ['-' for x in range(self.clength)]

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

        # the dictionary that holds the information about the tab; set defaults
        today = str(dt.date.today())
        self.info = {'filename': 'myTab.txt', 'title': 'My Tab', 'author':
                     'Me', 'date': today}

    def __str__(self):
        """Formatted string of the Tab object data
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
        """Format Tab object data for limited printing.

        This routine prints the tab object with the same formatting as calling
        `print(tab_instance)` but only three tab rows are printed: the row that
        the current chord position falls in and the two encapsulating rows
        (i.e. preceding and following rows).
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
            if i == num_loops:
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
        chord : list of str
            A list of single string characters of length self.clength that
            represents the chord
        index : int, optional
            The index of self.tab_data where the chord will be written.
            Default is the current index, self.i

        Returns
        -------
        None
        """
        # TODO I need to handle double digit fret numbers!!!

        # Check that the chord has the correct format
        if len(chord) != self.clength:
            # TODO fill out error information
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

    def backward(self, num=1):
        """Place the chord position back `num` places from where it currently
        is.


        Parameters
        ----------
        num : int, optional
            The number of places to go backwards in the tab. Must be an integer
            > 0. Default is 1.

        Returns
        -------
        None
        """

        if num < 0 or type(num) != int:
            raise TypeError('num argument must be an integer and > 0. num = '
                            '{}'.format(num))

        elif self.i - num < 0:
            raise IndexError('Requested backwards move is out of range. Index'
                             '= {:d}, and num = {:d}'.format(self.i, num))

        else:
            self.i -= num

    def forward(self, num=1):
        """Place the chord position forward `num` places from where it
        currently is.


        Parameters
        ----------
        num : int, optional
            The number of places to go forward in the tab. Must be an integer >
            0. Default is 1.

        Returns
        -------
        None
        """

        if num < 0 or type(num) != int:
            raise TypeError('num argument must be an integer and > 0. num = '
                            '{}'.format(num))

        # We can add to the present index without restriction as long as the
        # above is satisfied
        self.i += num

        # Check if the new index is greater than the previous maximum. If so,
        # the tab needs to be expanded
        if self.i > self.imax:
            self.tab_data += [self._blank for x in range(self.i - self.imax)]
            self.imax = self.i

# TODO present: check that this functions properly
    def set_info(self, **kwargs):
        """Set relevant information for the Tab object, such as author, date,
        etc.

        Parameters
        ----------
        filename : str
            The name of the file to which the tab should be read/written
        title : str
            The title of the tab
        author : str
            The author of the tab
        date : str
            The date the tab was written (str)

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

# TODO object IO should be handled in a separate module
    def get_tab(self, filename, overwrite_info=True, overwrite_data=True):
        """Open a guitab text file and extract the tab data from it.

        Parameters
        ----------
        filename : str
            The name of the file to read from
        overwrite_info: bool, optional
            A flag to decide if the current tab information should be
            overwritten with that contained in the file. 'True' to overwrite
            with file information, 'False' to retain the current tab
            information and so discard any information extracted from the file.
        overwrite_data: bool, optional
            If there is tab data held by the tab object instance, then this
            boolean flag determines if that data is overwritten by the data in
            the file.

        Returns
        -------
        data : list of list of str
            The tab data read from filename in a two-dimensional list object
            that is the internal storage format of the Tab object
        """

        error1 = 'Tab file incorrectly formatted: {}'
        error2 = 'Tab file incorrectly formatted or has mismatched tuning: {}'

        if type(overwrite_info) != bool:
            raise TypeError("overwrite_info argument in get_tab must be of "
                            "type bool. Type given: {}".format(overwrite_info.__class__))
        if type(overwrite_data) != bool:
            raise TypeError("overwrite_data argument in get_tab must be of "
                            "type bool. Type given: "
                            "{}".format(overwrite_data.__class__))

        with open(filename, 'r') as tabfile:

            if tabfile.readline() != (80 * '=' + '\n'):
                raise RuntimeError(error1.format(filename))

            # Get the tab information stored in this file
            info = {}
            for i in info_order:
                match = info_tests[i].search(tabfile.readline())
                if match:
                    info[i] = match.group(1)
                else:
                    raise RuntimeError(error1.format(filename))

            # Save the tab information in the tab instance if requested
            if overwrite_info:
                info['filename'] = filename
                self.set_info(**info)

            # Discard anything until the end of the header (allows for user
            # notes)
            while(True):
                line = tabfile.readline()
                if line == (80 * '=' + '\n'):
                    break
                elif line == '':
                    raise EOFError('EOF reached before finished reading header.')

            # Collect the tab data contained in the file
            data = []
            imax = 0
            while(True):

                line = tabfile.readline()

                if line == '\n':
                    continue

                elif line[0:2] == self._leader[0]:
                    rows = []
                    rows.append(line)
                    for i in range(1, self.clength):
                        line = tabfile.readline()
                        if line[0:2] == self._leader[i]:
                            rows.append(line)
                        else:
                            raise RuntimeError(error2.format(filename))
                    imax += len(rows[0]) - 3
                    for i in range(2, len(rows[0])-1):
                        chord = []
                        for j in range(self.clength):
                            chord.append(rows[j][i])
                        data.append(chord)

                elif line == '':
                    break

            if overwrite_data:
                self.tab_data = data
                self.imax = imax - 1

            return data

    # TODO think about encoding here? Current is 'us-ascii'
    def save_tab(self, filename=None, **kwargs):
        """Write the current tab data to a text file.


        Parameters
        ----------
        filename : str, optional
            The name of the file to write to. If not provided, the filename
            currently in the Tab object info is used.
        **kwargs : dict, optional
            title : the title of the tab (str)
            author : the author of the tab (str)
            date  : the date the tab was written (str)
        """

        # set the relevant tab info that has been passed to this function
        if filename is None:
            self.set_info(**kwargs)
        else:
            self.set_info(filename=filename, **kwargs)

        # check if the file already exists and give options
        # TODO move this to main CLI program, see NOTE for 2019-04-09
        tabfilename = self.info['filename']
        while(True):
            try:
                tabfile = open(tabfilename, 'x')
            except FileExistsError:
                message = "File already exists: '{}'\nOverwrite? [Y/n] ".format(tabfilename)
                inp = input(message)
                if inp.lower() == 'y':
                    tabfile = open(tabfilename, 'w')
                    break
                elif inp.lower() == 'n':
                    # TODO this is probably not security conscious; make more
                    # robust
                    inp2 = input('Please provide a different filename: ')
                    tabfilename = inp2
                    self.info['filename'] = inp2
                    continue
                else:
                    print('\nInvalid input. Please try again.')
                    continue
            else:
                break

        fileformat = 80 * '=' + '\n' + \
            'Title : {title}\n' + \
            'Author: {author}\n' + \
            'Date  : {date}\n' + \
            80 * '=' + '\n\n' + \
            '{tabdata}'

        # remove the current position character from the output of str(self)
        tabdata = rm_position.sub(r'\1 \2', str(self))

        # finally, write all relevant information to the file
        tabfile.write(fileformat.format(tabdata=tabdata, **self.info))

        tabfile.close()
