import pytest
from pydev import cities


@pytest.fixture()
def city_titles():
    """Dictionary mapping cities to page titles."""
    names = {
        'Austin': 'Austin, Texas',
        'Boulder': 'Boulder, Colorado',
        'Nashville': 'Nashville, Tennessee',
        'New York': 'New York City',
    }
    return names


def test_get_title(city_titles):
    """Test getting page titles for cities."""
    titles = [cities.get_city_title(name) for name in city_titles.keys()]
    correct = list(city_titles.values())
    assert titles == correct
