from ..tab import Tab
import pytest


@pytest.fixture
def blank_tab():
    return Tab()


# TODO manually create a partly filled tab for testing (i.e. independent of
# forward and backward methods)
@pytest.fixture
def filled_tab():
    return Tab()


def test_backward_out_of_bounds(blank_tab):
    """Check that going out of bounds with a `backward` operation yields
    IndexError."""
    with pytest.raises(IndexError):
        blank_tab.backward()
