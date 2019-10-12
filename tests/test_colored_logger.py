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
    test_name = "colored_logger"
    log_filepath = None

    @classmethod
    def setUpClass(cls):
        """TODO
        """
        super().setUpClass()
        # Setup logging
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)
        # Setup a console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        cls.logger.addHandler(ch)
        # Setup a file handler
        cls.log_filepath = os.path.join(cls.data_tmpdir, 'colored.log')
        fh = logging.FileHandler(cls.log_filepath)
        fh.setLevel(logging.DEBUG)
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)
        cls.logger.addHandler(fh)
        cls.logger.warning("Testing in the <color>{}</color> "
                           "environment".format(cls.logger._env))

    @classmethod
    def tearDownClass(cls):
        """TODO
        """
        # Read the log file before it is deleted
        log = read_file(cls.log_filepath)
        super().tearDownClass()
        # Check the log file
        if "<color>" in log or "</color>" in log:
            raise AssertionError("Tags were found in the log file")
        if log.count("\033"):
            raise AssertionError("Color codes were found in the log file")

    # @unittest.skip("test_add_color_to_msg()")
    def test_add_color_to_msg(self):
        """TODO
        """
        self.logger.info("\nTesting <color>_add_color_to_msg()</color>...")
        log_msg = "test"
        log_msg_with_tags = "<color>{}</color>".format(log_msg)
        log_level = "DEBUG"
        debug_color = self.logger._level_to_color[log_level]
        expected_output = "\x1b[{}m{}\x1b[0m".format(debug_color, log_msg)
        output = self.logger._add_color_to_msg(log_msg_with_tags, log_level)
        msg = "The log message '{}' is not as expected '{}'".format(
            output, expected_output)
        self.assertTrue(output == expected_output, msg)
        self.logger.info("The log message has the expected ANSI escape "
                         "sequence for coloring the message")

    # @unittest.skip("test_add_handlers_back()")
    def test_add_handlers_back(self):
        """TODO
        """
        self.logger.info("\nTesting <color>_add_removed_handlers()</color>...")
        # Setup test logger
        add_logger = self.setup_test_logging(name="test_add")
        # Setup console handler without adding it to the test logger
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # Add the handler to the logger's list of removed handlers
        add_logger._removed_handlers.append(ch)
        # Add the handler to the logger from the logger's list of removed handlers
        add_logger._add_handlers_back()
        # Assert that there is only one handler in the logger
        nb_handlers = len(add_logger.handlers)
        msg = "There should be only one handler but there are {} " \
              "handlers".format(nb_handlers)
        self.assertTrue(nb_handlers == 1, msg)
        self.logger.info("The console handler was successfully added")

    # @unittest.skip("test_all_logging_methods()")
    def test_all_logging_methods(self):
        """TODO
        """
        self.logger.info("\nTesting <color>all logging methods</color>...")
        # TODO: explain
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

    # @unittest.skip("test_keep_everything_but()")
    def test_keep_everything_but(self):
        """TODO
        """
        self.logger.info("\nTesting <color>_keep_everything_but</color>...")
        # Setup test logger
        keep_logger = self.setup_test_logging(name="test_keep",
                                              console_handler=True,
                                              file_handler=True)
        # Remove all handlers but the file handler
        keep_logger._keep_everything_but(handlers_to_remove=[logging.StreamHandler])
        # Assert that there is only one file handler in the test logger
        nb_handlers = len(keep_logger.handlers)
        msg = "There should be one handler in keep_logger but there are " \
              "{} handlers".format(nb_handlers)
        self.assertTrue(nb_handlers == 1, msg)
        # Make sure that the handler left is a file handler
        h = keep_logger.handlers[0]
        msg = "The remaining handler '{}' is not of the expected type " \
              "'{}'".format(h, logging.FileHandler)
        self.assertIsInstance(h, logging.FileHandler, msg)
        self.logger.info("Only the FileHandler is left in the logger")

    # @unittest.skip("test_remove_handler()")
    def test_remove_handler(self):
        """TODO
        """
        self.logger.info("\nTesting <color>_remove_handler()</color>...")
        # Setup test logger
        remove_logger = self.setup_test_logging(name="test_remove",
                                                console_handler=True)
        msg = "There should only be one handler in remove_logger"
        self.assertTrue(len(remove_logger.handlers) == 1, msg)
        # Remove the handler from the test logger
        ch = remove_logger.handlers[0]
        remove_logger._remove_handler(ch)
        # Assert that there should be no handler in the test logger
        nb_handlers = len(remove_logger.handlers)
        msg = "There should be no handler in remove_logger but there are " \
              "{} handlers".format(nb_handlers)
        self.assertTrue(nb_handlers == 0, msg)
        self.logger.info("The console handler was successfully removed")

    def setup_test_logging(self, name, console_handler=False, file_handler=False):
        """TODO

        Parameters
        ----------
        name
        console_handler
        file_handler

        Returns
        -------
        logger

        """
        # Setup logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if console_handler:
            # Setup console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            logger.addHandler(ch)
        if file_handler:
            # Setup file handler
            log_filepath = os.path.join(self.sandbox_tmpdir, 'test.log')
            fh = logging.FileHandler(log_filepath)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
        return logger


if __name__ == '__main__':
    unittest.main()
