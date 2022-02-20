from ..formatter import TabFormatter
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
