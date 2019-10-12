"""Module that defines tests for :mod:`~pyutils.logging_wrapper`

:class:`~pyutils.logging_wrapper.LoggingWrapper` and its methods are tested here.

"""

import logging
import unittest

from .utils import TestBase

logging.getLogger(__name__)  # .addHandler(logging.NullHandler)


class TestColoredLogging(TestBase):
    test_name = "colored_logging"

    @classmethod
    def setUpClass(cls):
        """TODO
        """
        super().setUpClass()
        # Setup logging
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)
        cls.logger.addHandler(ch)

    def test_logging(self):
        self.logger.info("INFO")


if __name__ == '__main__':
    unittest.main()
