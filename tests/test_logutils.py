"""Module that defines tests for :mod:`~pyutils.logutils`

Every functions in :mod:`~pyutils.logutils` are tested here.

The command to execute the :mod:`unittest` test runner::

    python -m unittest discover

This command is executed at the root of the project directory.

"""

import logging
import unittest
# Custom modules
from .logging_cfg import logging_cfg
from .utils import TestBase
from pyutils.logutils import get_error_msg, setup_logging


class TestFunctions(TestBase):

    TestBase.testname = "logutils"
    logging_cfg_path = "tests/logging_cfg.yaml"
    logging_cfg_dict = logging_cfg

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

    # @unittest.skip("test_setup_logging_case_1()")
    def test_setup_logging_case_1(self):
        """Test that setup_logging() can successfully setup logging from a
        YAML config file.

        This function tests that :meth:pyutils.logutils.setup_logging` TODO ...

        """
        print("\nTesting case 1 of get_error_msg()...")
        logger = logging.getLogger('scripts.scraper')
        # NOTE: if I put the next line inside the with, it will complain that
        # the expected log was not triggered on 'scripts.scraper'
        cfg_dict = setup_logging(self.logging_cfg_path)
        with self.assertLogs(logger, 'INFO') as cm:
            logger.info('first message')
        msg = "Log emitted not as expected"
        self.assertEqual(cm.output[0],
                         'INFO:scripts.scraper:first message',
                         msg)
        print("Log emitted as expected")
        msg = "The returned logging config dict doesn't have the expected keys"
        self.assertSequenceEqual(list(cfg_dict.keys()),
                                 list(self.logging_cfg_dict),
                                 msg)
        print("Logging setup successful!")


if __name__ == '__main__':
    unittest.main()
