"""TODO
"""

import logging
import os
from tempfile import TemporaryDirectory
import unittest

from pyutils.dbutils import create_db
from pyutils.genutils import create_dir, delete_folder_contents, read_file
from pyutils.logutils import setup_basic_logger


class TestBase(unittest.TestCase):
    # TODO
    TEST_MODULE_QUALNAME = None
    CREATE_TEST_DATABASE = False
    ADD_FILE_HANDLER = False
    LOGGER_NAME = __name__
    LOGGING_FILENAME = "debug.log"
    SHOW_FIRST_CHARS_IN_LOG = 1000
    SCHEMA_FILEPATH = None
    DB_FILENAME = "db.qlite"

    # Temporary directories
    _main_tmpdir_obj = None
    _main_tmpdir = None
    data_tmpdir = None
    sandbox_tmpdir = None
    # DB-related stuff
    db_filepath = None
    # Logging-related stuff
    logger = None
    log_filepath = None

    @classmethod
    def setUp(cls):
        """TODO
        """

    @classmethod
    def setUpClass(cls):
        """TODO
        """
        # Setup temporary directories
        cls.setup_tmp_dirs()
        # Setup logging for Test* instance
        cls.log_filepath = os.path.join(cls.data_tmpdir, cls.LOGGING_FILENAME)
        cls.logger = setup_basic_logger(
            name=cls.LOGGER_NAME,
            add_console_handler=True,
            add_file_handler=cls.ADD_FILE_HANDLER,
            log_filepath=cls.log_filepath,
            remove_all_handlers=True
        )
        # IMPORTANT: no printing before
        # Print name of module to be tested
        line_equals = "{}".format("=" * 92)
        line_name = "{}<color>{}</color>".format(" " * 37, cls.TEST_MODULE_QUALNAME)
        cls.logger.info("\n# {} #".format(line_equals))
        cls.logger.info(line_name)
        cls.logger.info("# {} #".format(line_equals))
        cls.logger.info("<color>Setting up {} tests...</color>".format(
            cls.TEST_MODULE_QUALNAME))
        # Print info about directories created
        cls.logger.info("Main temporary directory created: " + cls._main_tmpdir)
        cls.logger.info("Sandbox directory created: " + cls.sandbox_tmpdir)
        cls.logger.info("Data directory created: " + cls.data_tmpdir)
        # Create SQLite db
        if cls.CREATE_TEST_DATABASE:
            cls.db_filepath = os.path.join(cls.data_tmpdir, cls.DB_FILENAME)
            # NOTE: the logging is silenced for create_db
            create_db(cls.db_filepath, cls.SCHEMA_FILEPATH)
            cls.logger.warning("<color>SQLite database created:</color> "
                               "{}".format(cls.db_filepath))
        else:
            cls.logger.warning("<color>Database not used</color>")
        cls.logger.warning("ADD_FILE_HANDLER: <color>{}"
                           "</color>".format(cls.ADD_FILE_HANDLER))
        cls.logger.warning("SHOW_FIRST_CHARS_IN_LOG: <color>{}"
                           "</color>".format(cls.SHOW_FIRST_CHARS_IN_LOG))
        cls.logger.warning("Testing in the <color>{}</color> "
                           "environment".format(cls.logger._env))

    @classmethod
    def tearDown(cls):
        """TODO
        """
        cls.logger.info("Cleanup...")
        # Cleanup temporary directories
        # TODO: explain the if...
        if cls.sandbox_tmpdir:
            delete_folder_contents(cls.sandbox_tmpdir)

    @classmethod
    def tearDownClass(cls):
        """TODO
        """
        cls.logger.info("\n")
        if cls.ADD_FILE_HANDLER and cls.log_filepath and \
                cls.SHOW_FIRST_CHARS_IN_LOG:
            # Read the log file before it is deleted
            log = read_file(cls.log_filepath).strip("\n")
            # Check the log file
            if "<color>" in log or "</color>" in log:
                raise AssertionError("Tags were found in the log file")
            if log.count("\033"):
                raise AssertionError("Color codes were found in the log file")
            cls.logger.warning("<color>Content of the log file (first {} chars):"
                               "</color>".format(cls.SHOW_FIRST_CHARS_IN_LOG))
            cls.logger.info(log[:cls.SHOW_FIRST_CHARS_IN_LOG])
            line_dashes = "{}".format("-" * 70)
            cls.logger.info("{}\n".format(line_dashes))
        cls.logger.info("<color>Final cleanup...</color>")
        # Delete the temporary directory
        cls._main_tmpdir_obj.cleanup()
        cls.logger.warning("<color>All temporary directories deleted</color>")
        # Close all handlers, especially if it is a file handler, or you might
        # get the following error:
        # "ResourceWarning: unclosed file <_io.TextIOWrapper
        # name='...colored.log' mode='a' encoding='UTF-8'>"
        for h in cls.logger.handlers:
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
        self.logger.info("<color>Log emitted as expected:</color> " + output)
        return retcode

    def log_test_method_name(self):
        """TODO
        """
        self.logger.warning("\n<color>{}()</color>".format(
            self.__dict__['_testMethodName']))
