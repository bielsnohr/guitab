import filecmp
from pathlib import Path
from ..formatter import TabFormatter, TxtTabFormatter
import pytest
from . import global_test_data


@pytest.fixture
def blank_tab_formatter(monkeypatch):
    # patch the TabFormatter ABC so that it can be instantiated
    monkeypatch.setattr(TabFormatter, '__abstractmethods__', set())
    return TabFormatter()


def test_valid_set_metadata(blank_tab_formatter):
    """Check that the set_metadata() method of the ABC TabFormatter correctly sets tab metadata"""
    blank_tab_formatter.set_metadata(**global_test_data.tab_info)
    assert blank_tab_formatter._tab_metadata == global_test_data.tab_info


def test_valid_set_data(blank_tab_formatter):
    """Check that the set_data() method of the ABC TabFormatter correctly sets tab data"""
    blank_tab_formatter.set_data(global_test_data.tab_data)
    assert blank_tab_formatter._tab_data == global_test_data.tab_data


def test_valid_get_data(blank_tab_formatter: TabFormatter):
    """Check that the get_data() method of the ABC TabFormatter correctly retrieves tab data"""
    blank_tab_formatter._tab_data = global_test_data.tab_data
    assert blank_tab_formatter.get_data() == global_test_data.tab_data


def test_TxtTabFormatter_write_formatted_tab(tmp_path):
    """Check that the TxtTabFormatter writes a properly formatted textual
    representation of the tab to the output stream
    """
    save_file = tmp_path / "test_guitab_file.txt"
    txt_formatter = TxtTabFormatter()
    txt_formatter.set_metadata(**global_test_data.tab_info)
    txt_formatter.set_data(global_test_data.tab_data)
    with open(save_file, mode='x') as fileobj:
        txt_formatter._write_formatted_tab(fileobj=fileobj)
    assert filecmp.cmp(save_file, Path(__file__).parent / "test_guitab_file.txt")
