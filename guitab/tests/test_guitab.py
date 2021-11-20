from ..guitab import GuitabShell
import re
from . import global_test_data
from pathlib import Path


welcome_message = r"Welcome to guitab, an interactive command line program "\
    r"that accelerates the tab writing process. Type help or \? to list "\
    r"commands."


def test_guitab_welcome_message_and_quit(monkeypatch, capsys):
    """Confirm that the custom shell program displays a welcome message and
    then quits"""

    # monkeypatch the "input" function, so that it returns predefined input.
    # This simulates the user entering this input in the terminal
    user_input = iter(['bye'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_input))
    guitab_shell = GuitabShell()
    guitab_shell.cmdloop()
    out, err = capsys.readouterr()
    welcome_message_re = re.compile(welcome_message + r"\nThank you for using guitab\n")
    assert welcome_message_re.match(out)


# TODO this test needs to be more rigorous
def test_guitab_help_message(monkeypatch, capfd):
    """Confirm that the custom shell program displays a help message and
    then quits"""

    user_input = iter(['help', 'bye'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_input))
    guitab_shell = GuitabShell()
    guitab_shell.cmdloop()
    out, err = capfd.readouterr()
    help_message_regex = re.compile(welcome_message +
                                    r"\n\nDocumented commands \(type help <topic>\):\n"
                                    r"========================================\n")
    assert help_message_regex.match(out)


def test_guitab_print_tab_blank(capfd):
    """Confirm that the custom shell program displays a blank tab correctly and
    then quits"""

    guitab_shell = GuitabShell()
    guitab_shell.do_print('')
    out, err = capfd.readouterr()
    assert out == global_test_data.print_blank_tab


def test_guitab_print_tab_2_rows(monkeypatch, capfd):
    """Confirm that the custom shell program displays a 2 row tab correctly and
    then quits"""

    guitab_shell = GuitabShell()
    guitab_shell.do_forward("78")
    out, err = capfd.readouterr()
    assert out == global_test_data.print_tab_2_rows


def test_guitab_forward_no_arg(monkeypatch, capfd):
    """Confirm that the custom shell program handles no argument to the chord
    command correctly"""

    guitab_shell = GuitabShell()
    guitab_shell.do_forward('')
    out, err = capfd.readouterr()
    assert out == global_test_data.print_tab_1_forward


def test_guitab_write_chord(capfd):
    """Confirm that the custom shell program can write a C chord, display it
    correctly and then quit"""

    guitab_shell = GuitabShell()
    guitab_shell.do_chord("- 1 - 2 3 x")
    out, err = capfd.readouterr()
    assert out == global_test_data.print_tab_c_chord


def test_guitab_write_invalid_chord(capfd):
    """Confirm that the correct warning message is generated when passing
    invalid chord input to the write command"""

    guitab_shell = GuitabShell()
    guitab_shell.do_chord("")
    out, err = capfd.readouterr()
    assert out == "Invalid number of finger positions provided: 0. Expected 6.\n"
    guitab_shell.do_chord("t t t t t t")
    out, err = capfd.readouterr()
    assert out == "Invalid finger position provided: t\n"


def test_guitab_load():
    """Confirm that the custom shell program can correctly load tab data"""

    test_file = Path(__file__).parent / "test_guitab_file.txt"
    guitab_shell = GuitabShell()
    guitab_shell.do_load(str(test_file))
    assert str(guitab_shell.user_tab) == global_test_data.str_tab_file_load


def test_guitab_loadall():
    """Confirm that the custom shell program can correctly load tab data"""

    test_file = Path(__file__).parent / "test_guitab_file.txt"
    guitab_shell = GuitabShell()
    guitab_shell.do_loadall(str(test_file))
    assert str(guitab_shell.user_tab) == global_test_data.str_tab_file_load
    assert guitab_shell.user_tab.info == global_test_data.file_info
