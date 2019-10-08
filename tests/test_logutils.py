"""Module that defines tests for :mod:`~pyutils.logutils`

Every functions in :mod:`~pyutils.logutils` are tested here.

The command to execute the :mod:`unittest` test runner::

    python -m unittest discover

This command is executed at the root of the project directory.

"""

import unittest
# Custom modules
from .utils import TestBase
from pyutils.logutils import get_error_msg, setup_logging


class TestFunctions(TestBase):

    TestBase.testname = "logutils"

    # @unittest.skip("test_get_error_msg()")
    def test_get_error_msg(self):
        """Test that get_error_msg() returns an error message.

        This function tests that :meth:pyutils.logutils.get_error_msg` returns
        an error message from an exception.

        """
        print("Testing get_error_msg()...")
        exc = IOError("The file doesn't exist")
        error_msg = get_error_msg(exc)
        expected = "[OSError] The file doesn't exist"
        msg = "The error message '{}' is different from the expected one " \
              "'{}'".format(error_msg, expected)
        self.assertTrue(error_msg == expected, msg)
        print("The error message is the expected one")


if __name__ == '__main__':
    unittest.main()
