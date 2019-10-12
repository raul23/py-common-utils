"""Module that defines tests for :mod:`~pyutils.logging_wrapper`

:class:`~pyutils.logging_wrapper.LoggingWrapper` and its methods are tested here.

"""

import logging
import os
import unittest

from .utils import TestBase
from pyutils.genutils import read_file

logging.getLogger(__name__).addHandler(logging.NullHandler)


class TestColoredLogging(TestBase):
    test_name = "colored_logging"
    log_filepath = None

    @classmethod
    def setUpClass(cls):
        """TODO
        """
        super().setUpClass()
        # Setup logging
        # Setup a console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)
        cls.logger.addHandler(ch)
        # Setup a file handler
        cls.log_filepath = os.path.join(cls.data_tmpdir, 'colored.log')
        fh = logging.FileHandler(cls.log_filepath)
        fh.setLevel(logging.DEBUG)
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)
        cls.logger.addHandler(fh)
        cls.logger.warning("Testing in the <color>{}</color> environment".format(cls.logger._env))

    @classmethod
    def tearDownClass(cls):
        """TODO
        """
        # Read the log file before it is deleted
        log = read_file(cls.log_filepath)
        super().tearDownClass()
        # Check the log file
        if log.count("<color>") and log.count("</color>"):
            raise AssertionError("Tags were found in the log file")
        if log.count("\033"):
            raise AssertionError("Color codes were found in the log file")

    def test_add_color_to_msg(self):
        """TODO
        """
        print("Testing _add_color_to_msg()...")
        if self.logger._env == "PROD":
            expected_output = "\x1b[36mtest\x1b[0m"
        else:
            expected_output = "\x1b[34mtest\x1b[0m"
        output = self.logger._add_color_to_msg("test", "DEBUG")
        msg = "The log message '{}' is not as expected '{}'".format(
            output, expected_output)
        self.assertTrue(output == expected_output, msg)
        self.logger.info("The log message has the expected ANSI escape "
                         "sequence for coloring the message")

    def test_all_logging_methods(self):
        """TODO
        """
        print("\nTesting all logging methods...")
        # IMPORTANT: TODO capture logs, logs to console and file not shown
        with self.assertLogs(self.logger, "DEBUG") as cm:
            self.logger.debug("DEBUG")
            self.logger.info("INFO")
            self.logger.warning("WARNING")
            # Deprecated method
            self.logger.warn("WARN")
            self.logger.critical("CRITICAL")
            self.logger.fatal("FATAL")
        expected_output = ['DEBUG:tests.test_colored_logger:DEBUG',
                           'INFO:tests.test_colored_logger:INFO',
                           'WARNING:tests.test_colored_logger:WARNING',
                           'WARNING:tests.test_colored_logger:WARN',
                           'CRITICAL:tests.test_colored_logger:CRITICAL',
                           'CRITICAL:tests.test_colored_logger:FATAL']
        self.assertListEqual(cm.output, expected_output)
        self.logger.info("All logging methods logged the expected messages")


if __name__ == '__main__':
    unittest.main()
