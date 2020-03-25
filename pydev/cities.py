"""Analysis of cities based on data from Wikipedia.

This module downloads Wikipedia descriptions of cities, which are then
encoded into vector representations using the Universal Sentence
Encoder from Tensorflow Hub. These vectors can then be compared to
get a quantitative estimate of how similar cities are based on their
Wikipedia text.

Use compare_cities to compare a reference city to a list of other
cities.
"""

import numpy as np
from scipy.spatial import distance
import pandas as pd
import wikipedia
import tensorflow_hub as hub


def load_use_model(version='standard'):
    """Load the univeral sentence encoder from Tensorflow Hub."""

    if version == 'standard':
        module_url = 'https://tfhub.dev/google/universal-sentence-encoder/4'
    elif version == 'lite':
        module_url = 'https://tfhub.dev/google/universal-sentence-encoder-lite/2'
    else:
        raise ValueError(f'Unknown version: {version}')

    model = hub.load(module_url)
    return model


def get_city_title(city_name):
    """Convert city name to Wikipedia page title."""

    names = {'Austin': 'Austin, Texas',
             'Boulder': 'Boulder, Colorado',
             'Nashville': 'Nashville, Tennessee',
             'New York': 'New York City'}
    if city_name in names:
        title = names[city_name]
    else:
        # look for an exact match
        results = wikipedia.search(city_name)
        if city_name in results:
            title = city_name
        else:
            print(f'No exact match for {city_name}. Search results:')
            for name in results:
                print(name)
            raise ValueError('City title not found.')
    return title


def city_summary(page_title, sentences=None):
    """Download a text summary of a city from Wikipedia."""

    summary = wikipedia.summary(page_title, sentences=sentences)
    return summary


def city_vector(name, model, sentences=None):
    """Get a vector corresponding to a city summary."""

    title = get_city_title(name)
    summary = city_summary(title, sentences)
    vector = model([summary])
    return vector


def compare_cities(reference_city, comparison_cities, model=None,
                   model_version='standard'):
    """Compare a reference city to a list of comparison cities."""

    if model is None:
        model = load_use_model(model_version)
    reference = city_vector(reference_city, model).numpy()
    comparison = np.vstack([city_vector(name, model).numpy()
                            for name in comparison_cities])
    similarity = 1 - distance.cdist(reference, comparison, 'correlation')
    results = pd.Series(similarity[0], index=comparison_cities)
    return results