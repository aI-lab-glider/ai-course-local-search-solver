class AlgortihmError(Exception):
    """
    Base class for errors that could be thrown by an algorithm.
    """


class NoSolutionFoundError(AlgortihmError):
    """
    No solution exists for this problem.
    """
