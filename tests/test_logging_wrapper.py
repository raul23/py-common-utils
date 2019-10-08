"""Module that defines tests for :mod:`~pyutils.logging_wrapper`

:class:`~pyutils.logging_wrapper.LoggingWrapper` and its methods are tested here.

"""

import unittest
# Custom modules
from .utils import TestBase


class TestFunctions(TestBase):
    test_name = "logging_wrapper"


if __name__ == '__main__':
    unittest.main()
