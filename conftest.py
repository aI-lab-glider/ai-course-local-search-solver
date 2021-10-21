import numpy
import random as rand

import pytest


@pytest.fixture
def random():
    rand.seed(0)
    numpy.random.seed(0)