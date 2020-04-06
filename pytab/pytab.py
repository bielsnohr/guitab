#!/usr/bin/env python
"""
Author: Matthew Bluteau <matthew.bluteau@gmail.com>
Version: 1.0
Description: An interacive command line program that speeds up the process of
    writing guitar tabs. The user enters chords/fingering count by count with
    the final result being written to a text file.
"""

import argparse
import tab
import os


def main():

    print("Welcome to pyTab, an interactive command line program that "
          "accelerates the tab writing process. Type -h or --help for "
          "details of how to run the program.")

    allowed = ['-', 'h', 'p', 'x'] + [str(x) for x in range(25)]

    # define the argument parser object
    parser = argparse.ArgumentParser(prog='pyTab', description='TODO:'
                                     'fill in description of pyTab')

    # TODO the string with space issue requires nargs='+' to solve. Check
    #      how this impact all of the arguments
    # TODO add an argument that can take in single letter chord names and
    # produce the correct tab representation
    # TODO add argument for setting the title of the tab
    parser.add_argument('-c', '--chord', nargs=6, choices=allowed, help='The'
                        ' chord/fingering for the current count. If'
                        ' present, there must be 6 positional arguments'
                        '--one for each string. Input order runs from high '
                        'e to low E.')
    parser.add_argument('-q', nargs='+', type=str, const=True,
                        help='Save tab then quit pyTab. Name of file'
                        ' can be set as optional argument.')
    parser.add_argument('-d', action='store_true', help='Flag'
                        ' to quit pyTab without saving progress.')
    parser.add_argument('-p', action='store_true', help='Flag'
                        ' to print the entirety of the current tab.')
    parser.add_argument('-b', nargs='?', const=1, type=int, help='The'
                        ' number of counts to go back in the tab '
                        '(the default is 1 if the flag is present).')
    parser.add_argument('-f', nargs='?', const=1, type=int, help='The'
                        ' number of counts to go forward in the tab '
                        '(the default is 1 if the flag is present).')
    parser.add_argument('-o', '--outfile', nargs='+', type=str,
                        default=None, help='The file for the tab'
                        ' to be written to.')
    parser.add_argument('-t', '--title', nargs='+', type=str,
                        default=None, help='The title of the tab to be'
                        ' stored in the output file.')
    parser.add_argument('-a', '--author', nargs='+', type=str,
                        default=None, help='The name of the tab author to be'
                        ' stored in the output file.')
    parser.add_argument('-D', '--date', nargs=1, type=str,
                        default=None, help='The date associated with the tab '
                        ' that will be stored in the output file. Defaults '
                        'to today\'s date')
    parser.add_argument('-s', '--save', nargs='+', type=str,
                        const=True, help='Save the tab to file. Name of file'
                        ' can be set as optional argument.')
    parser.add_argument('-l', '--load', nargs=1, type=str,
                        default=None, help='Load a tab from the filename '
                        'argument. Any tab metadata (author, etc) from the '
                        'current pyTab session will not be overwritten.')
    parser.add_argument('-L', '--loadall', nargs=1, type=str,
                        default=None, help='Load a tab and all metadata from '
                        'the filename argument. Any tab metadata (author, etc)'
                        ' from the current pyTab session will be overwritten.')

    # Initialize the tab object and any other relevant variables (although
    # these should be soon implemented in the tab class itself) before entering
    # main program loop
    user_tab = tab.Tab()

    while(True):

        inp = input('[pyTab]: ')

        try:
            args = parser.parse_args(inp.split())
            #print(args)
        except:
            continue

        # Quit without saving
        if args.d:
            break

        # Set the file name
        if args.outfile is not None:
            user_tab.set_info(filename=' '.join(args.outfile))

        # Set the author name
        if args.author is not None:
            user_tab.set_info(filename=' '.join(args.author))

        # Set the date
        if args.date is not None:
            user_tab.set_info(filename=args.date[0])

        # Set the title
        if args.title is not None:
            user_tab.set_info(filename=' '.join(args.title))

        # Save and quit
        if args.q:
            if args.q is True:
                user_tab.save_tab()
                break
            else:
                user_tab.save_tab(filename=' '.join(args.q))
                break

        # Save file and set filename if given
        if args.save:
            if args.save is True:
                user_tab.save_tab()
            else:
                user_tab.save_tab(filename=' '.join(args.save))
        
        # TODO add loading tab functionality

        # Print a paginated version of the whole tab
        # TODO need to make this OS agnostic because it uses `less` command
        if args.p:
            pipe = os.popen('less', mode='w')
            print(user_tab, file=pipe)
            pipe.close()
        
        # Move current position backwards in tab
        if args.b:
            try:
                user_tab.backward(args.b)
            except (TypeError, IndexError) as inst:
                print(inst)
                continue
            user_tab.print()

        # Move current position forwards in tab
        if args.f:
            try:
                user_tab.forward(args.f)
            except TypeError as inst:
                print(inst)
                continue
            user_tab.print()

        # Write a chord to the current position
        if args.chord:
            try:
                user_tab.write(args.chord)
            except TypeError as inst:
                print(inst)
                continue
            user_tab.print()



if __name__ == "__main__":
    main()
