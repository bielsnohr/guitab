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
import tab


def main():
    print("Welcome to pyTab, an interactive command line program that "
          "accelerates the tab writing process. Type -h or --help for "
          "details of how to run.")
    allowed = ['-', 'h', 'p', 'x'] + [str(x) for x in range(25)]
    flag = True
    # define the argument parser object
    parser = argparse.ArgumentParser(prog='pyTab', description='TO-DO:'
                                     'fill in description of pyTab')
    parser.add_argument('-c', '--chord', nargs=6, choices=allowed, help=
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
    parser.add_argument('-f', nargs='?', const=1, type=int, help='the'
                        ' number of counts to go forward in the tab '
                        '(the default is 1 if the flag is present)')
    parser.add_argument('-o', type=argparse.FileType('a'),
                        default='mytab.txt', help='the file for the tab'
                        ' to be written to')
    # URGENT: need to modify the argument parser so that the 6 positional
    # arguments are optional (will probably have to make them optional
    # arguments instead of positional)
    # TO-DO: add an option for inputting a title, add an option for adding
    # the author to the file, add option for quitting without saving
    # progress

    while(True):
        #if newtab:
        #    tab = cp.deepcopy(blank)
        #    newtab = False

        inp = input('[pyTab]: ')

        try:
            args = parser.parse_args(inp.split())
        except:
            continue

        # could read in the input file and check for a header to see if a
        # header needs to be written
        if flag:
            args.o.write("Header for pyTab Tab\n")
            # initiate the tab for the first time
            x = tab.tab()
            # TO-DO: add more information to this like author, filename, date
            flag = False
        if args.d:
            # write current tab buffer to file
            args.o.write('\n' + str(x))
            args.o.close()
            break
        if args.b is not None:
            x.back(args.b)
            continue
        if args.f is not None:
            x.forward(args.f)
            continue
        elif len(args.chord) != 6:
            print('You must enter 6 positional arguments when specifying a'
                  ' count.\nPlease try again.')
            # Raise a type error here instead? This would necessitate a new
            # class for lists of length 6? Or just a simple type error...
            continue
        else:
            # Now, we want to write to the tab
            if x.write(args.chord):
                args.o.write('\n' + str(x))
                print("Starting new line...")
                # reset the tab to initial settings
                x.__init__()


if __name__ == "__main__":
    main()
