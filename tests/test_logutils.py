"""Module that defines tests for :mod:`~pyutils.logutils`

Every functions in :mod:`~pyutils.logutils` are tested here.

"""

from copy import deepcopy
import logging
import unittest
# Custom modules
from .utils import TestBase
from pyutils.logutils import get_error_msg, setup_logging


class TestFunctions(TestBase):
    # TODO
    test_name = "logutils"

    # @unittest.skip("test_get_error_msg()")
    def test_get_error_msg(self):
        """Test that get_error_msg() returns an error message.

        This function tests that :meth:`~pyutils.logutils.get_error_msg` returns
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

    def setup_logging_for_testing(self, logging_cfg):
        """Setup logging for testing from a logging config file or dict.

        Depending on `logging_cfg`, this function setups logging for testing
        from a logging config file or dict.

        Parameters
        ----------
        logging_cfg

        Notes
        -----
        This function is called by :meth:`test_setup_logging_case_1` and
        :meth:`test_setup_logging_case_2`.

        """
        # NOTE: if I put the next line inside the with, it will complain that
        # the expected log was not triggered on 'scripts.scraper'
        ret_cfg_dict = setup_logging(logging_cfg)
        logger = logging.getLogger('scripts.scraper')
        with self.assertLogs(logger, 'INFO') as cm:
            logger.info('first message')
        msg = "Log emitted not as expected"
        self.assertEqual(cm.output[0],
                         'INFO:scripts.scraper:first message',
                         msg)
        print("Log emitted as expected")
        msg = "The returned logging config dict doesn't have the expected keys"
        self.assertSequenceEqual(list(ret_cfg_dict.keys()),
                                 list(self.logging_cfg_dict),
                                 msg)
        how = "dict" if isinstance(logging_cfg, dict) else "file"
        print("Successfully setup logging with the logging config "
              "{}!".format(how))

    # @unittest.skip("test_setup_logging_case_1()")
    def test_setup_logging_case_1(self):
        """Test that setup_logging() can successfully setup logging from a
        YAML config file.

        Case 1 tests that :meth:`~pyutils.logutils.setup_logging` TODO ...

        """
        print("\nTesting case 1 of setup_logging()...")
        self.setup_logging_for_testing(self.logging_cfg_path)

    # @unittest.skip("test_setup_logging_case_2()")
    def test_setup_logging_case_2(self):
        """Test that setup_logging() can successfully setup logging from a dict.

        Case 2 tests that :meth:`~pyutils.logutils.setup_logging` TODO ...

        """
        print("\nTesting case 2 of setup_logging()...")
        self.setup_logging_for_testing(self.logging_cfg_dict)

    # @unittest.skip("test_setup_logging_case_3()")
    def test_setup_logging_case_3(self):
        """Test setup_logging() when the logging config file doesn't exist.

        Case 3 tests that :meth:`~pyutils.logutils.setup_logging` raises an
        :exc:`OSError` exception when the logging config file doesn't exist.

        """
        print("\nTesting case 3 of setup_logging()...")
        with self.assertRaises(OSError):
            setup_logging("bad_logging_config.yaml")
        print("Raised an OSError exception as expected")

    # @unittest.skip("test_setup_logging_case_4()")
    def test_setup_logging_case_4(self):
        """Test setup_logging() when the logging config dict has an invalid
        value.

        Case 4 tests that :meth:`~pyutils.logutils.setup_logging` raises an
        :exc:`ValueError` exception when the logging config dict is invalid,
        e.g. a logging handler's class is written incorrectly.

        """
        print("\nTesting case 4 of setup_logging()...")
        # Corrupt a logging handler's class
        # NOTE: if I use copy instead of deepcopy, logging_cfg will also
        # reflect the corrupted handler's class
        corrupted_cfg = deepcopy(self.logging_cfg_dict)
        corrupted_cfg['handlers']['console']['class'] = 'bad.handler.class'
        # Setup logging with the corrupted config dict
        with self.assertRaises(ValueError):
            setup_logging(corrupted_cfg)
        print("Raised a ValueError exception as expected")

    # @unittest.skip("test_setup_logging_case_5()")
    def test_setup_logging_case_5(self):
        """Test setup_logging() when the logging config dict is missing an
        important key.

        Case 5 tests that :meth:`~pyutils.logutils.setup_logging` raises a
        :exc:`KeyError` exception when the logging config dict is missing an
        important key, i.e. a key that is needed in
        :meth:`~pyutils.logutils.setup_logging`.

        """
        print("\nTesting case 5 of setup_logging()...")
        # Remove a key from the logging config dict
        corrupted_cfg = deepcopy(self.logging_cfg_dict)
        expected_missing_key = 'handlers'
        del corrupted_cfg[expected_missing_key]
        # Setup logging with the corrupted config dict
        with self.assertRaises(KeyError) as cm:
            setup_logging(corrupted_cfg)
        missing_key = cm.exception.args[0]
        msg = "The actual missing key ('{}') is not the expected one " \
              "('{}')".format(missing_key, expected_missing_key)
        self.assertTrue(expected_missing_key == missing_key, msg)
        print("Raised a KeyError exception as expected")


if __name__ == '__main__':
    unittest.main()
