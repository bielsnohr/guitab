from ..tab import Tab
import pytest
import datetime as dt


@pytest.fixture
def blank_tab():
    return Tab()


@pytest.fixture
def filled_tab_dict():
    return {'_MAX': 78, 'clength': 6, '_blank':
            ['-', '-', '-', '-', '-', '-'],
            'tab_data':
            [['-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-']],
            '_leader': ('e|', 'B|', 'G|', 'D|', 'A|', 'E|'),
            'allowed':
            ['-', 'h', 'p', 'x', '0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
             '18', '19', '20', '21', '22', '23', '24'],
            'i': 3, 'imax': 3,
            'info': {'filename': 'myTab.txt', 'title': 'My Tab',
                     'author': 'Me', 'date': str(dt.date.today())}}


@pytest.fixture
def filled_tab(filled_tab_dict):
    filled_tab = Tab()
    filled_tab.tab_data = filled_tab_dict['tab_data']
    filled_tab.i = filled_tab_dict['i']
    filled_tab.imax = filled_tab_dict['imax']
    return filled_tab


def test_backward_out_of_bounds(blank_tab):
    """Check that going out of bounds with a `backward` operation yields
    IndexError."""
    with pytest.raises(IndexError):
        blank_tab.backward()


def test_backward_valid(filled_tab, filled_tab_dict):
    """Check that valid `backward` operation yields expected tab state."""
    filled_tab.backward()
    filled_tab_dict['i'] = 2
    assert filled_tab.__dict__ == filled_tab_dict


def test_forward_valid(blank_tab, filled_tab_dict):
    """Check that valid `forward` operation yields expected tab state."""
    blank_tab.forward(3)
    assert blank_tab.__dict__ == filled_tab_dict


def test_write_current(filled_tab, filled_tab_dict):
    """Check that writing a chord to the current index (default no index
    specified) yields the correct tab"""
    chord = ['-', '1', '-', '2', '3', 'x']
    filled_tab_dict['tab_data'][filled_tab_dict['i']] = chord
    filled_tab.write(chord)
    assert filled_tab.__dict__ == filled_tab_dict


def test_write_lower_index(filled_tab, filled_tab_dict):
    """Check that writing a chord to a lower index than the current one yields
    the correct tab"""
    chord = ['-', '1', '-', '2', '3', 'x']
    index = 1
    filled_tab_dict['tab_data'][index] = chord
    filled_tab.write(chord, index=index)
    assert filled_tab.__dict__ == filled_tab_dict


def test_write_higher_index(filled_tab, filled_tab_dict):
    """Check that writing a chord to a higher index than the current one yields
    the correct tab"""
    chord = ['-', '1', '-', '2', '3', 'x']
    index = 10
    [filled_tab_dict['tab_data'].append(filled_tab_dict['_blank']) for x in
     range(7)]
    filled_tab_dict['tab_data'][index] = chord
    filled_tab_dict['imax'] = index
    filled_tab.write(chord, index=index)
    assert filled_tab.__dict__ == filled_tab_dict


@pytest.mark.parametrize('invalid_tab', [
    ['-', '-', '-', '-', '-', '-', '-'],
    ['r', 'z', '-', '-', '-', '-']
])
def test_write_invalid_chord(invalid_tab, filled_tab):
    """Check that writing an invalid chord raises a TypeError"""
    with pytest.raises(TypeError):
        filled_tab.write(invalid_tab)
