import numpy
import random as rand

import pytest


@pytest.fixture
def set_random_seed():
    rand.seed(0)
    numpy.random.seed(0)
