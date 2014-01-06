#!/usr/bin/env python
'''
@name: /Users/Matt/Google Drive/Python_workspace/Python_practice/pyTab.py
@author: Matt
@date: Nov 25, 2013
@version: 0.1
@description: An interacive command line program that speeds up the process of
    writing guitar tabs. The user enters chords/fingering count by count with
    the final result being written to a text file.
'''
# TO-DO: add better functionality for loading previous tabs (other than just
# appending to the input file given as below)

import argparse
import numpy as np
import copy as cp
import re

# Set up a blank tab to be copied each time at the beginning of each iteration
# of main()
blank = np.zeros((6, 80), dtype='U2')
blank[:, :] = '-'
blank[:, 0] = ('e', 'B', 'G', 'D', 'A', 'E')
blank[:, 1] = '|'


def main():
    print("Welcome to pyTab, an interactive command line program that "
          "accelerates the tab writing process. Type -h or --help for "
          "details of how to run.")
    allowed = ['-', 'h', 'p', 'x'] + [str(x) for x in range(25)]
    flag = True
    newtab = True
    i = 2
    max_ind = max(blank.shape)

    while(True):
        if newtab:
            tab = cp.deepcopy(blank)
            newtab = False

        inp = input('[pyTab]: ')

        parser = argparse.ArgumentParser(prog='pyTab', description='TO-DO:'
                                         'fill in description of pyTab')
        parser.add_argument('chord', nargs='*', choices=allowed, help=
                            'the chord/fingering for the current count (if'
                            ' present, there must be 6 positional arguments'
                            '-one for each string). Input order runs from high '
                            'e to low e', default='-')
                            #default=['-', '-', '-', '-', '-', '-'])
        parser.add_argument('-d', action='store_true', help='flag'
                            ' to quit pyTab and save progress')
        parser.add_argument('-b', nargs='?', const=1, type=int, help='the'
                            ' number of counts to go back in the tab '
                            '(the default is 1 if the flag is present)')
        parser.add_argument('-o', type=argparse.FileType('a'),
                            default='mytab.txt', help='the file for the tab'
                            ' to be written to')
        # TO-DO: add an option for inputting a title, add an option for adding
        # the author to the file, add option for adding blank chord, 
        try:
            args = parser.parse_args(inp.split())
        except:
            print("Your input wasn't correct. Please try again...")
            continue

        # could read in the input file and check for a header to see if a
        # header needs to be written
        if flag:
            args.o.write("Header for pyTab Tab")
            # TO-DO: add more information to this like author, filename, date
            flag = False
        if args.d:
            # write current tab buffer to file
            tab_text = re.sub('(\[\[)|(\]\])|(\s)|(\')', '',
                         str(tab)).replace('][', '\n')
            args.o.write('\n' + tab_text)
            args.o.close()
            break
        elif len(args.chord) != 6:
            print('You must enter 6 positional arguments when specifying a'
                  ' count.\nPlease try again.')
            # Raise a type error here instead? This would necessitate a new
            # class for lists of length 6?
            continue
        else:
            # Now, we want to start writing the tab, but I need the numpy array
            # template that I want to edit... what is the most efficient way
            # to get this starting template? Use copy.deepcopy? or make a new
            # class that defines a "clone" method and essentially just returns
            # a copy of itself via this method...
            tab[:, i] = args.chord
            tab_text = re.sub('(\[\[)|(\]\])|(\s)|(\')', '',
                         str(tab)).replace('][', '\n')
            print(tab_text)
            i = i + 1
            if i > max_ind:
                args.o.write('\n' + tab_text)
                print("Starting new line...")
                newtab = True
                i = 2


if __name__ == "__main__":
    main()
