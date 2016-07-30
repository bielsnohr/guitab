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
# TODO:
# 1. add an option for inputting a title, add an option for adding
# the author to the file, add option for quitting without saving
# progress
#
# 2. Store the tab numpy arrays in a list/other array. This way, we don't
# need to select the file until the program is quit (i.e. the file will
# only be written to once). Furthermore, this array of tabs should be
# pickled so it can be read in for subsequent runs of the program

import argparse
import tab
import os


def main():
    print("Welcome to pyTab, an interactive command line program that "
          "accelerates the tab writing process. Type -h or --help for "
          "details of how to run.")
    allowed = ['-', 'h', 'p', 'x'] + [str(x) for x in range(25)]
    #flag = True
    # define the argument parser object
    parser = argparse.ArgumentParser(prog='pyTab', description='TO-DO:'
                                     'fill in description of pyTab')
    parser.add_argument('-c', '--chord', nargs=6, choices=allowed, help='the'
                        ' chord/fingering for the current count (if'
                        ' present, there must be 6 positional arguments'
                        '-one for each string). Input order runs from high '
                        'e to low E', default='-')
    parser.add_argument('-d', action='store_true', help='flag'
                        ' to quit pyTab and save progress')
    parser.add_argument('-b', nargs='?', const=1, type=int, help='the'
                        ' number of counts to go back in the tab '
                        '(the default is 1 if the flag is present)')
    parser.add_argument('-f', nargs='?', const=1, type=int, help='the'
                        ' number of counts to go forward in the tab '
                        '(the default is 1 if the flag is present)')
    parser.add_argument('-o', '--outfile', nargs=1, type=str,
                        default=None, help='the file for the tab'
                        ' to be written to')

    # Initialize the tab object and any other relevant variables (although
    # these should be soon implemented in the tab class itself) before entering
    # main program loop
    x = tab.tab()
    outfile = False

    while(True):

        inp = input('[pyTab]: ')

        try:
            args = parser.parse_args(inp.split())
            #print(args)
        except:
            continue

        if args.outfile is not None:
            if os.path.isfile(args.outfile):
                outfile = open(args.outfile, mode='a')
            else:
                outfile = open(args.outfile, mode='r')
                outfile.write("Header for pyTab Tab\n\n")
        if args.d:
            # write current tab buffer to file
            if args.outfile is not None:
                outfile.write('\n' + str(x))
                outfile.close()
            break
        if args.b is not None:
            x.back(args.b)
            continue
        if args.f is not None:
            x.forward(args.f)
            continue
        if args.chord is '-':
            continue
        else:
            # Now, we want to write to the tab
            if x.write(args.chord):
                outfile.write('\n' + str(x) + '\n')
                print("Starting new line...")
                # reset the tab to initial settings
                x.__init__()


if __name__ == "__main__":
    main()
