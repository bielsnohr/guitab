#!/usr/bin/env python
"""An interacive command line program that speeds up the process of writing
guitar tabs.

The user enters chords/fingering count by count with the final
result being written to a text file.
"""

import argparse
import os
import cmd

from . import tab


# TODO it looks like Cmd will pass a blank string rather than None if no
# arguments are given to a command. I need to modify argument parsing below and
# tests to account for this.
class GuitabShell(cmd.Cmd):

    intro = "Welcome to guitab, an interactive command line program "\
        "that accelerates the tab writing process. Type help or ? to list "\
        "commands."
    prompt = '(guitab) '
    file = None

    # ----- initialise ---------
    def __init__(self, completekey='tab', stdin=None, stdout=None) -> None:
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        self.user_tab = tab.Tab()

    # ----- functional commands -----
    def move(self, direction, arg):
        if arg != '':
            try:
                num = int(arg)
                self.user_tab.__getattribute__(direction.lower())(num=num)
            except ValueError:
                print(direction.upper() + " requires a single integer input. Given: " + arg, file=self.stdout)
                return
        else:
            self.user_tab.__getattribute__(direction.lower())(num=1)

        self.user_tab.print()

    def do_forward(self, arg):
        """The number of counts to go forward in the tab:  FORWARD 10

        The default is to move forward 1 space if no input is given to the command.
        """
        self.move("forward", arg)

    def do_backward(self, arg):
        """The number of counts to go backward in the tab:  BACKWARD 10

        The default is to move back 1 space if no input is given to the command.
        """
        self.move("backward", arg)

    def do_chord(self, arg):
        """The chord (i.e. finger positions) to write to the current position in the tab:  CHORD x 3 2 0 1 0

        The input order of strings runs from high E to low E.
        """
        try:
            arg = arg.split()
        except Exception:
            print("ERROR: Invalid argument string to CHORD", file=self.stdout)
            return
        try:
            self.user_tab.write(arg)
            self.user_tab.print()
        except TypeError as e:
            print(e, file=self.stdout)

    # ----- utility functions -----
    def do_bye(self, arg):
        """Stop editing tab and exit:  BYE

        The current tab is saved to a file if one has been previously specified by RECORD.
        """
        print('Thank you for using guitab')
        self.close()
        return True

    # TODO this is OS dependent and should be extended for mac and Windows
    def do_print(self, arg):
        """Print the entirety of the tab: PRINT"""
        pipe = os.popen('less', mode='w')
        print(self.user_tab, file=pipe)
        pipe.close()

    # ----- file handling -----
    def do_load(self, arg: str):
        """Load only tab data from specified file (not metadata)

        Parameters
        ----------
        arg : str
            File name for file to load tab data from

        Returns
        -------
        None
        """
        if arg == '':
            print("ERROR: The LOAD command requires an argument", file=self.stdout)
            return
        else:
            self.user_tab.get_tab(arg, overwrite_info=False)

    def do_loadall(self, arg: str):
        """Load tab data and metadata from specified file

        Parameters
        ----------
        arg : str
            File name for file to load tab data from

        Returns
        -------
        None
        """
        if arg is None:
            print("ERROR: The LOADALL command requires an argument", file=self.stdout)
            return
        else:
            self.user_tab.get_tab(arg, overwrite_info=True)

    # ----- customisation -----
    def onecmd(self, line: str) -> bool:
        """Catch acceptable exceptions caused by users"""
        try:
            val = super().onecmd(line)
        except IndexError as e:
            print(e, file=self.stdout)
        else:
            return val

    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')

    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())

    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


def main():
    """Main function for guitab module

    This initiates a REPL-like program that takes in user input to build the
    tablature using a `Tab` object
    """

    print("Welcome to guitab, an interactive command line program that "
          "accelerates the tab writing process. Type -h or --help for "
          "details of how to run the program.")

    # TODO this should be set in the tab class, not here
    allowed = ['-', 'h', 'p', 'x'] + [str(x) for x in range(25)]

    # define the argument parser object
    parser = argparse.ArgumentParser(prog='guitab',
                                     description='description of guitab')

    # TODO add an argument that can take in single letter chord names
    parser.add_argument('-c', '--chord', nargs=6, choices=allowed, help='The'
                        ' chord/fingering for the current count. If'
                        ' present, there must be 6 positional arguments'
                        '--one for each string. Input order runs from high '
                        'e to low E.')
    parser.add_argument('-q', nargs='*', type=str,
                        help='Save tab then quit guitab. Name of file'
                        ' can be set as optional argument.')
    parser.add_argument('-d', action='store_true', help='Flag'
                        ' to quit guitab without saving progress.')
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
                        ' that will be stored in the output file. ISO format. '
                        'Today\'s date will be used for tab if not set.')
    parser.add_argument('-s', '--save', nargs='*', type=str,
                        help='Save the tab to file. Name of file'
                        ' can be set as optional argument.')
    parser.add_argument('-l', '--load', nargs='+', type=str,
                        default=None, help='Load a tab from the filename '
                        'argument. Any tab metadata (author, etc) from the '
                        'current guitab session will not be overwritten.')
    parser.add_argument('-L', '--loadall', nargs='+', type=str,
                        default=None, help='Load a tab and all metadata from '
                        'the filename argument. Any tab metadata (author, etc)'
                        ' from the current guitab session will be overwritten.')

    # Initialize the tab object and any other relevant variables (although
    # these should be soon implemented in the tab class itself) before entering
    # main program loop
    user_tab = tab.Tab()

    while True:

        inp = input('[tab]: ')

        try:
            args = parser.parse_args(inp.split())
        except BaseException:
            continue

        # Quit without saving
        if args.d:
            break

        # Set the file name
        if args.outfile:
            user_tab.set_info(filename=' '.join(args.outfile))

        # Set the author name
        if args.author:
            user_tab.set_info(author=' '.join(args.author))

        # Set the date
        if args.date:
            user_tab.set_info(date=args.date[0])

        # Set the title
        if args.title:
            user_tab.set_info(title=' '.join(args.title))

        # Save and quit
        if args.q is not None:
            if len(args.q) == 0:
                user_tab.save_tab()
                break
            else:
                user_tab.save_tab(filename=' '.join(args.q))
                break

        # Save file and set filename if given
        if args.save is not None:
            if len(args.save) == 0:
                user_tab.save_tab()
            else:
                user_tab.save_tab(filename=' '.join(args.save))

        # Print the entirety of the tab
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

        # Load the tab but don't overwrite metadata
        if args.load:
            user_tab.get_tab(' '.join(args.load), overwrite_info=False)

        # Load the tab and overwrite metadata
        if args.loadall:
            user_tab.get_tab(' '.join(args.loadall))


if __name__ == '__main__':
    GuitabShell().cmdloop()
