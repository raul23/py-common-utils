"""Module that defines tests for :mod:`~pyutils.logging_wrapper`

:class:`~pyutils.logging_wrapper.LoggingWrapper` and its methods are tested here.

"""

import logging
import os
import unittest

from .utils import TestBase
from pyutils.genutils import read_file
from pyutils.logutils import setup_basic_logger

logging.getLogger(__name__).addHandler(logging.NullHandler)


class TestColoredLogging(TestBase):
    # TODO
    test_module_name = "colored_logger"
    log_filepath = None
    ADD_FILE_HANDLER = True
    LOGGING_FILENAME = "colored.log"
    SHOW_FIRST_CHARS_IN_LOG = 1000

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
        cls.logger.warning("\n<color>Content of the log file (first {} chars):"
                           "</color>".format(cls.SHOW_FIRST_CHARS_IN_LOG))
        cls.logger.info(log[:cls.SHOW_FIRST_CHARS_IN_LOG])

    # @unittest.skip("test_add_color_to_msg()")
    def test_add_color_to_msg(self):
        """TODO
        """
        self.logger.warning("\n<color>test_add_color_to_msg()</color>")
        self.logger.info("Testing <color>_add_color_to_msg()</color>...")
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
        self.logger.warning("\n\n<color>test_add_handlers_back()</color>")
        self.logger.info("Testing <color>_add_removed_handlers()</color>...")
        # Setup test logger
        add_logger = setup_basic_logger(name="test_add")
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
        self.logger.warning("\n\n<color>test_all_logging_methods()</color>")
        self.logger.info("Testing <color>all logging methods</color>...")
        # TODO: explain
        # IMPORTANT: TODO capture logs, logs to console and file not shown
        with self.assertLogs(self.logger, "DEBUG") as cm:
            self.logger.debug("DEBUG")
            self.logger.info("INFO")
            self.logger.warning("WARNING")
            # Deprecated method
            self.logger.warn("WARN")
            try:
                test = "abc " + 123
            except TypeError as e:
                self.logger.exception(e, exc_info=True)
            self.logger.critical("CRITICAL")
            self.logger.fatal("FATAL")
        expected_messages = [
            'DEBUG', 'INFO', 'WARNING', 'WARN', 'CRITICAL', 'FATAL'
        ]
        message = [r.message for r in cm.records if "TypeError" not in r.message]
        self.assertListEqual(message, expected_messages)
        exc_msg = [r.message for r in cm.records if "TypeError" in r.message]
        msg = "There should only be one exception message"
        self.assertTrue(len(exc_msg) == 1, msg)
        exc_msg = exc_msg[0]
        self.logger.error("Exception message: <color>{}</color>".format(exc_msg))
        self.logger.info("All logging methods logged the expected messages")

    # @unittest.skip("test_found_tags()")
    def test_found_tags(self):
        """TODO
        """
        self.logger.warning("\n\n<color>test_found_tags()</color>")
        self.logger.info("Testing <color>_found_tags()</color>...")
        log_msg1 = "Hello, <color>World</color>!"
        log_msg2 = "Hello, World!"
        found = self.logger._found_tags(log_msg1)
        msg = "No tags were found in the log message: {}".format(log_msg1)
        self.assertTrue(found, msg)
        found = self.logger._found_tags(log_msg2)
        msg = "Tags were found in the log message: {}".format(log_msg2)
        self.assertFalse(found, msg)

    # @unittest.skip("test_keep_everything_but()")
    def test_keep_everything_but(self):
        """TODO
        """
        self.logger.warning("\n\n<color>test_keep_everything_but()</color>")
        self.logger.info("Testing <color>_keep_everything_but()</color> "
                         "(StreamHandler)...")
        # Setup test logger
        log_filepath = os.path.join(self.sandbox_tmpdir, 'test.log')
        keep_logger = setup_basic_logger(
            name="test_keep_everything_but",
            add_console_handler=True,
            add_file_handler=True,
            log_filepath=log_filepath)
        # Keep only the file handler. The rests of handlers should be removed
        keep_logger._keep_everything_but(
            handlers_to_remove=[logging.StreamHandler])
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

    # @unittest.skip("test_remove_all_tags()")
    def test_remove_all_tags(self):
        """TODO
        """
        self.logger.warning("\n\n<color>test_remove_all_tags()</color>")
        self.logger.info("Testing <color>_remove_all_tags()</color>...")
        log_msg = "<log>Hello, <color>World</color>!</log>"
        raw_log_msg = self.logger._remove_all_tags(log_msg)
        found = self.logger._found_tags(raw_log_msg)
        msg = "Tags were found in the log message: {}".format(raw_log_msg)
        self.assertFalse(found, msg)

    # @unittest.skip("test_remove_everything_but()")
    def test_remove_everything_but(self):
        """TODO
        """
        self.logger.warning("\n\n<color>test_remove_everything_but()</color>")
        self.logger.info("Testing <color>_remove_everything_but()</color> "
                         "(StreamHandler)...")
        # Setup test logger
        log_filepath = os.path.join(self.sandbox_tmpdir, 'test.log')
        remove_logger = setup_basic_logger(
            name="test_remove_everything_but",
            add_console_handler=True,
            add_file_handler=True,
            log_filepath=log_filepath)
        # Remove all handlers but the console handler
        remove_logger._remove_everything_but(
            handlers_to_keep=[logging.StreamHandler])
        # Assert that there is only one console handler in the test logger
        nb_handlers = len(remove_logger.handlers)
        msg = "There should be one handler in keep_logger but there are " \
              "{} handlers".format(nb_handlers)
        self.assertTrue(nb_handlers == 1, msg)
        # Make sure that the handler left is a console handler
        h = remove_logger.handlers[0]
        msg = "The remaining handler '{}' is not of the expected type " \
              "'{}'".format(h, logging.StreamHandler)
        self.assertIsInstance(h, logging.StreamHandler, msg)
        self.logger.info("Only the StreamHandler is left in the logger")

    # @unittest.skip("test_remove_handler()")
    def test_remove_handler(self):
        """TODO
        """
        self.logger.warning("\n\n<color>test_remove_handler()</color>")
        self.logger.info("Testing <color>_remove_handler()</color>...")
        # Setup test logger
        log_filepath = os.path.join(self.sandbox_tmpdir, 'test.log')
        remove_logger = setup_basic_logger(
            name="test_remove",
            add_console_handler=True,
            log_filepath=log_filepath)
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


if __name__ == '__main__':
    unittest.main()
