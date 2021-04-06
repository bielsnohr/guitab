from ..guitab import main
import pytest
import re
from . import global_test_data


welcome_message = "Welcome to guitab, an interactive command line program "\
        "that accelerates the tab writing process. Type -h or --help for "\
        "details of how to run the program.\n"


def test_guitab_welcome_message_and_quit(monkeypatch, capfd):
    """Confirm that the custom shell program displays a welcome message and
    then quits"""

    # monkeypatch the "input" function, so that it returns predefined input.
    # This simulates the user entering this input in the terminal
    user_input = iter(['-d'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_input))
    main()
    out, err = capfd.readouterr()
    assert out == welcome_message


# TODO this test needs to be more rigorous
def test_guitab_help_message(monkeypatch, capfd):
    """Confirm that the custom shell program displays a help message and
    then quits"""

    user_input = iter(['-h', '-d'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_input))
    main()
    out, err = capfd.readouterr()
    help_message_regex = re.compile(welcome_message + r"usage: guitab \[-h\]")
    assert help_message_regex.search(out)


def test_guitab_print_tab_blank(monkeypatch, capfd):
    """Confirm that the custom shell program displays a blank tab correctly and
    then quits"""

    user_input = iter(['-p', '-d'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_input))
    main()
    out, err = capfd.readouterr()
    assert out == welcome_message + global_test_data.print_blank_tab


def test_guitab_print_tab_2_rows(monkeypatch, capfd):
    """Confirm that the custom shell program displays a 2 row tab correctly and
    then quits"""

    user_input = iter(['-f 78', '-d'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_input))
    main()
    out, err = capfd.readouterr()
    assert out == welcome_message + global_test_data.print_tab_2_rows


def test_guitab_write_chord(monkeypatch, capfd):
    """Confirm that the custom shell program can write a C chord, display it
    correctly and then quit"""

    user_input = iter(['-c - 1 - 2 3 x', '-d'])
    monkeypatch.setattr('builtins.input', lambda _: next(user_input))
    main()
    out, err = capfd.readouterr()
    assert out == welcome_message + global_test_data.print_tab_c_chord
