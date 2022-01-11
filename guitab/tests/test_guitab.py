from ..guitab import GuitabShell
import re
from . import global_test_data
from pathlib import Path
import filecmp


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


def test_guitab_set_author():
    """Confirm that the custom shell program sets the author metadata"""

    guitab_shell = GuitabShell()
    author_name = "John Doe"
    guitab_shell.do_author(author_name)
    assert guitab_shell.user_tab.info['author'] == author_name


def test_guitab_set_title():
    """Confirm that the custom shell program sets the title metadata"""

    guitab_shell = GuitabShell()
    tab_title = "The Best Song in the World"
    guitab_shell.do_title(tab_title)
    assert guitab_shell.user_tab.info['title'] == tab_title


def test_guitab_set_date():
    """Confirm that the custom shell program sets the date metadata"""

    guitab_shell = GuitabShell()
    tab_date = '2022-01-09'
    guitab_shell.do_date(tab_date)
    assert guitab_shell.user_tab.info['date'] == tab_date


def test_guitab_bad_date(capfd):
    """Confirm that the custom shell a bad date string"""

    guitab_shell = GuitabShell()
    tab_date = '09-01-2021'
    guitab_shell.do_date(tab_date)
    out, err = capfd.readouterr()
    assert out == "ERROR: Incorrect date string. Must be of format YYYY-MM-DD.\n"


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


def test_guitab_load_noarg(capfd):
    """Confirm that the custom shell program correctly handles no arg to LOAD command"""

    guitab_shell = GuitabShell()
    guitab_shell.do_load('')
    out, err = capfd.readouterr()
    assert out == "ERROR: The LOAD command requires an argument\n"


def test_guitab_loadall():
    """Confirm that the custom shell program can correctly load tab data"""

    test_file = Path(__file__).parent / "test_guitab_file.txt"
    guitab_shell = GuitabShell()
    guitab_shell.do_loadall(str(test_file))
    assert str(guitab_shell.user_tab) == global_test_data.str_tab_file_load
    assert guitab_shell.user_tab.info == global_test_data.file_info


def test_guitab_save(tmp_path):
    """Confirm that the custom shell program can correctly save tab data"""

    save_file = tmp_path / "test_guitab_file.txt"
    guitab_shell = GuitabShell()
    guitab_shell.user_tab.info = {key: val for key, val in global_test_data.file_info.items()}
    guitab_shell.user_tab.write(['-', '1', '-', '2', '3', 'x'])
    guitab_shell.user_tab.write(['3', '3', '-', '-', '2', '3'], index=81)
    guitab_shell.do_save(str(save_file))
    assert filecmp.cmp(save_file, Path(__file__).parent / "test_guitab_file.txt")


def test_guitab_incorrect_save(capfd):
    """Confirm that the custom shell program throws an error message for incorrect save"""

    guitab_shell = GuitabShell()
    guitab_shell.do_save('')
    out, err = capfd.readouterr()
    assert out == "ERROR: The SAVE command requires an argument if a file hasn't been set previously\n"
