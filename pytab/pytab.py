#!/usr/bin/env python
"""
Author: Matthew Bluteau <matthew.bluteau@gmail.com>
Version: 1.0
Description: An interacive command line program that speeds up the process of
    writing guitar tabs. The user enters chords/fingering count by count with
    the final result being written to a text file.
"""
# TODO:
# 1. add an option for inputting a title, add an option for adding
# the author to the file, add option for quitting without saving
# progress
# 
# 2. I need to think about how to keep notes of the design decisions and with
# each commit I make. Should this all go in the commit message? Surely I need a
# rough space that I can work out thoughts and then reference these to the git
# commit history so it is easier to compose a changelog when it comes to a
# release
#

import argparse
import tab
import os


def main():
    print("Welcome to pyTab, an interactive command line program that "
          "accelerates the tab writing process. Type -h or --help for "
          "details of how to run the program.")
    allowed = ['-', 'h', 'p', 'x'] + [str(x) for x in range(25)]
    #blank = ['-' for i in range(6)]
    #flag = True
    # define the argument parser object
    parser = argparse.ArgumentParser(prog='pyTab', description='TO-DO:'
                                     'fill in description of pyTab')

    # TODO add an argument that can take in single letter chord names and
    # produce the correct tab representation
    parser.add_argument('-c', '--chord', nargs=6, choices=allowed, help='the'
                        ' chord/fingering for the current count (if'
                        ' present, there must be 6 positional arguments'
                        '-one for each string). Input order runs from high '
                        'e to low E')
    parser.add_argument('-d', action='store_true', help='flag'
                        ' to quit pyTab and save progress')
    parser.add_argument('-p', action='store_true', help='flag'
                        ' to print the entirety of the current tab')
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
    x = tab.Tab()
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

        if args.p:
            pipe = os.popen('less', mode='w')
            print(x, file=pipe)
            pipe.close()
        
        if args.b:
            try:
                x.backward(args.b)
            except (TypeError, IndexError) as inst:
                print(inst)
            continue

        if args.f:
            try:
                x.forward(args.f)
            except TypeError as inst:
                print(inst)
            continue

        if args.chord:
            try:
                x.write(args.chord)
            except TypeError as inst:
                print(inst)
            continue



if __name__ == "__main__":
    main()
