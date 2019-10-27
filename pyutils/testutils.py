"""TODO
"""

import functools
import logging
import os
import sys
import unittest
from logging import NullHandler
from tempfile import TemporaryDirectory

from pyutils.dbutils import create_db
from pyutils.genutils import create_dir, delete_folder_contents, read_file
from pyutils.logutils import setup_basic_logger

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def surround_signs(func):
    """TODO

    Returns
    -------

    """

    @functools.wraps(func)
    def call_func(self, *args, **kwargs):
        self.log_signs()
        result = func(self, *args, **kwargs)
        self.log_signs()
        return result

    return call_func


class TestBase(unittest.TestCase):
    # TODO
    TEST_MODULE_QUALNAME = None
    CREATE_TEST_DATABASE = False
    ADD_FILE_HANDLER = False
    LOGGER_NAME = __name__
    LOGGING_FILENAME = "debug.log"
    SHOW_FIRST_CHARS_IN_LOG = 1000
    SCHEMA_FILEPATH = None
    # TODO: call it TEST_DB_FILENAME
    DB_FILENAME = "db.qlite"

    env_type = "DEV" if bool(os.environ.get("PYCHARM_HOSTED")) else "PROD"
    _meth_names = None
    # Temporary directories
    _main_tmpdir_obj = None
    _main_tmpdir = None
    data_tmpdir = None
    sandbox_tmpdir = None
    # DB-related stuff
    # TODO: call it test_db_filepath
    db_filepath = None
    # Logging-related stuff
    logger = None
    log_filepath = None
    # Others
    _start_newline = True

    @classmethod
    def setUp(cls):
        """TODO
        Ref.: https://stackoverflow.com/a/56381855
        """
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")

    @classmethod
    def setUpClass(cls):
        """TODO
        """
        # TODO: explain
        cls.meth_names = [k for k in cls.__dict__.keys() if k.startswith("test")]
        cls.meth_names.sort()
        # Setup temporary directories
        cls.setup_tmp_dirs()
        # Filepath where the log file will be saved
        cls.log_filepath = os.path.join(cls.data_tmpdir, cls.LOGGING_FILENAME)
        # Setup logging for TestBase
        setup_basic_logger(
            name=__name__,
            add_console_handler=True,
            # console_format= "%(name)-42s: %(levelname)-8s %(message)s",
            add_file_handler=cls.ADD_FILE_HANDLER,
            log_filepath=cls.log_filepath,
            remove_all_handlers=True)
        # Setup logging for instance of TestBase
        setup_basic_logger(
            name=cls.LOGGER_NAME,
            add_console_handler=True,
            # console_format="%(name)-42s: %(levelname)-8s %(message)s",
            add_file_handler=cls.ADD_FILE_HANDLER,
            log_filepath=cls.log_filepath,
            remove_all_handlers=True)
        # IMPORTANT: no printing before
        # Print name of module to be tested
        line_equals = "{}".format("=" * 92)
        line_name = "{}<color>{}</color>".format(" " * 37,
                                                 cls.TEST_MODULE_QUALNAME)
        logger.info("\n# {} #".format(line_equals))
        logger.info(line_name)
        logger.info("# {} #".format(line_equals))
        logger.info("<color>Setting up {} tests...</color>".format(
            cls.TEST_MODULE_QUALNAME))
        # Print info about directories created
        logger.info("Main temporary directory created: " + cls._main_tmpdir)
        logger.info("Sandbox directory created: " + cls.sandbox_tmpdir)
        logger.info("Data directory created: " + cls.data_tmpdir)
        # Create SQLite db
        if cls.CREATE_TEST_DATABASE:
            cls.db_filepath = os.path.join(cls.data_tmpdir, cls.DB_FILENAME)
            # NOTE: the logging is silenced for create_db
            create_db(cls.db_filepath, cls.SCHEMA_FILEPATH)
            logger.warning("<color>SQLite database created:</color> "
                           "{}".format(cls.db_filepath))
        else:
            logger.warning("<color>Database not used</color>")
        logger.warning("<color>ADD_FILE_HANDLER:</color> "
                       "{}".format(cls.ADD_FILE_HANDLER))
        logger.warning("<color>SHOW_FIRST_CHARS_IN_LOG:</color> "
                       "{}".format(cls.SHOW_FIRST_CHARS_IN_LOG))
        logger.warning("Testing in the <color>{}</color> "
                       "environment".format(cls.env_type))

    @classmethod
    def tearDown(cls):
        """TODO
        """
        logger.info("Cleanup...")
        # Cleanup temporary directories
        # TODO: explain the if...
        if cls.sandbox_tmpdir:
            delete_folder_contents(cls.sandbox_tmpdir)

    @classmethod
    def tearDownClass(cls):
        """TODO
        """
        # TODO: explain
        logger.info("\n")
        if cls.ADD_FILE_HANDLER and cls.log_filepath and \
                cls.SHOW_FIRST_CHARS_IN_LOG:
            # Read the log file before it is deleted
            log = read_file(cls.log_filepath).strip("\n")
            # Check the log file
            if "<color>" in log or "</color>" in log:
                raise AssertionError("Tags were found in the log file")
            if log.count("\033"):
                raise AssertionError("Color codes were found in the log file")
            logger.warning("<color>Content of the log file (first {} chars):"
                           "</color>".format(cls.SHOW_FIRST_CHARS_IN_LOG))
            logger.info(log[:cls.SHOW_FIRST_CHARS_IN_LOG])
            line_dashes = "{}".format("-" * 70)
            logger.info("{}\n".format(line_dashes))
        logger.info("<color>Final cleanup...</color>")
        # Delete the temporary directory
        cls._main_tmpdir_obj.cleanup()
        logger.warning("<color>All temporary directories deleted</color>")
        # Close all handlers, especially if it is a file handler, or you might
        # get the following error:
        # "ResourceWarning: unclosed file <_io.TextIOWrapper
        # name='...colored.log' mode='a' encoding='UTF-8'>"
        for h in logger.handlers:
            h.close()

    @classmethod
    def setup_tmp_dirs(cls):
        """TODO
        """
        # Create main temporary directory
        cls._main_tmpdir_obj = TemporaryDirectory()
        cls._main_tmpdir = cls._main_tmpdir_obj.name
        # Create sandbox directory where the methods can write
        cls.sandbox_tmpdir = create_dir(
             os.path.join(cls._main_tmpdir, "sandbox"))
        # Create a directory for data files (e.g. SQLite database) useful
        # for performing the tests
        cls.data_tmpdir = create_dir(os.path.join(cls._main_tmpdir, "data"))

    # TODO: Where is it used?
    def assert_logs(self, logger, level, str_to_find, fnc, *args, **kwargs):
        """TODO

        Parameters
        ----------
        logger : logging.Logger
        level : str
        str_to_find : str
        fnc
        *args
        **kwargs

        Returns
        -------
        retcode : int

        """
        # TODO: explain
        with self.assertLogs(logger, level) as cm:
            retcode = fnc(*args, **kwargs)
        found = False
        output = None
        for o in cm.output:
            if o.find(str_to_find) != -1:
                found = True
                output = o
                break
        msg = "'{}' not found in logs".format(str_to_find)
        self.assertTrue(found and output, msg)
        logger.info("<color>Log emitted as expected:</color> " + output)
        return retcode

    def log_main_message(self, extra_msg=None):
        """TODO

        Parameters
        ----------
        extra_msg

        """
        self.log_test_method_name()
        case, cfg_func = self.parse_test_method_name()
        info_msg = "Case <color>{}</color> of testing <color>{}()" \
                   "</color>".format(case, cfg_func)
        info_msg += "\n{}".format(extra_msg) if extra_msg else ""
        logger.info(info_msg)

    def log_signs(self, sign='#', times=96):
        """TODO

        Parameters
        ----------
        sign
        times

        """
        num_signs = "<color>{}</color>".format(sign * times)
        logger.info(num_signs)

    def log_test_method_name(self):
        """TODO
        """
        # TODO: explain
        warning_msg = "{}<color>{}()</color>".format(
            "\n" if self._start_newline else "",
            self._testMethodName)
        if self.meth_names[0] == self._testMethodName:
            logger.warning(warning_msg)
        else:
            logger.warning("\n{}".format(warning_msg))

    def parse_test_method_name(self):
        """TODO

        Returns
        -------

        """
        case = self._testMethodName.split("case_")[-1]
        config_func = self._testMethodName.split("test_")[1].split("_case")[0]
        return case, config_func

    @surround_signs
    def call_func(self, func, *args, **kwargs):
        """TODO

        Parameters
        ----------
        func
        args
        kwargs

        Returns
        -------

        """
        result = func(*args, **kwargs)
        return result
