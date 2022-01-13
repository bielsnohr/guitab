#!/usr/bin/env python
"""An interacive command line program that speeds up the process of writing
guitar tabs.

The user enters chords/fingering count by count with the final
result being written to a text file.
"""

import os
import cmd
from datetime import datetime as dt

from . import tab


class GuitabShell(cmd.Cmd):

    intro = "Welcome to guitab, an interactive command line program "\
        "that accelerates the tab writing process. Type help or ? to list "\
        "commands."
    prompt = '(guitab) '

    # ----- initialise ---------
    def __init__(self, completekey='tab', stdin=None, stdout=None) -> None:
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        self.user_tab = tab.Tab()
        # TODO tidy up how this file parameter is used below and how the file name in general is retained
        self.file = None

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

    # TODO extend this to take single letter chord names
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

    def do_author(self, arg: str):
        """Set the author for the tab

        Parameters
        ----------
        arg : str
            Author name

        Returns
        -------
        None
        """
        self.set_info(key='author', value=arg)

    def do_title(self, arg: str):
        """Set the title for the tab

        Parameters
        ----------
        arg : str
            Title of the tab

        Returns
        -------
        None
        """
        self.set_info(key='title', value=arg)

    def do_date(self, arg: str):
        """Set the date for the tab

        Parameters
        ----------
        arg : str
            Date the tab was created or updated in ISO 8601 format (i.e. YYYY-MM-DD)

        Returns
        -------
        None
        """
        try:
            dt.strptime(arg, '%Y-%m-%d')
        except ValueError:
            print("ERROR: Incorrect date string. Must be of format YYYY-MM-DD.", file=self.stdout)
        else:
            self.set_info(key='date', value=arg)

    def set_info(self, key: str, value: str):
        if value == '':
            print("ERROR: The {key.upper()} command requires an argument", file=self.stdout)
            return
        else:
            self.user_tab.set_info(**{key: value})

    # ----- utility functions -----
    def do_bye(self, arg):
        """Stop editing tab and exit:  BYE

        The current tab is saved to a file if one has been previously specified by RECORD.
        """
        print('Thank you for using guitab', file=self.stdout)
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
        if arg == '':
            print("ERROR: The LOADALL command requires an argument", file=self.stdout)
            return
        else:
            self.user_tab.get_tab(arg, overwrite_info=True)

    def do_save(self, arg: str):
        """Save tab data and metadata to specified file

        Parameters
        ----------
        arg : str
            File name for file to save tab data to

        Returns
        -------
        None
        """
        if arg == '':
            if self.file is None:
                print("ERROR: The SAVE command requires an argument if a file hasn't been set previously",
                      file=self.stdout)
                return
            else:
                self.user_tab.save_tab(filename=self.file)
        else:
            self.user_tab.save_tab(filename=arg)
            self.file = arg

    # ----- customisation -----
    def onecmd(self, line: str) -> bool:
        """Catch acceptable exceptions caused by users"""
        try:
            val = super().onecmd(line)
        except IndexError as e:
            print(e, file=self.stdout)
        else:
            return val

    def precmd(self, line):
        return line.lower()


if __name__ == '__main__':
    GuitabShell().cmdloop()
