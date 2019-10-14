"""TODO

"""

import logging
import os
from tempfile import TemporaryDirectory
import unittest

from .data.logging import logging_cfg_dict
from pyutils.dbutils import create_db
from pyutils.genutils import create_dir, delete_folder_contents
from pyutils.logutils import setup_basic_logger


class TestBase(unittest.TestCase):
    # TODO
    test_module_name = None
    CREATE_TEST_DATABASE = False

    # Temporary directories
    _main_tmpdir_obj = None
    _main_tmpdir = None
    data_tmpdir = None
    sandbox_tmpdir = None
    # DB-related stuff
    schema_filepath = "tests/data/music.sql"
    db_filepath = None
    # Logging-related stuff
    logger = None
    ini_logging_cfg_path = "tests/data/logging.ini"
    yaml_logging_cfg_path = "tests/data/logging.yaml"
    logging_cfg_dict = logging_cfg_dict

    @classmethod
    def setUp(cls):
        """TODO
        """
        print()

    @classmethod
    def setUpClass(cls):
        """TODO
        """
        # Setup logging for TestFunctions
        cls.logger = setup_basic_logger(
            name=__name__,
            add_console_handler=True,
            handlers_to_remove=[logging.NullHandler]
        )
        # Print name of module to be tested
        line_equals = "# {} #".format("=" * 92)
        line_name = "{}<color>{}</color>".format(" " * 37, cls.test_module_name)
        cls.logger.info("\n" + line_equals)
        cls.logger.info(line_name)
        cls.logger.info(line_equals)
        cls.logger.info("<color>Setting up {} tests...</color>".format(
            cls.test_module_name))
        # Setup temporary directories
        cls.setup_tmp_dirs()
        if cls.CREATE_TEST_DATABASE:
            # Create SQLite db
            cls.db_filepath = os.path.join(cls.data_tmpdir, "db.sqlite")
            # NOTE: the logging is silenced for create_db
            create_db(cls.db_filepath, cls.schema_filepath)
            cls.logger.info("SQLite database created: " + cls.db_filepath)

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
        cls.logger.info("\n\n<color>Final cleanup...</color>")
        # Delete the temporary directory
        cls._main_tmpdir_obj.cleanup()
        cls.logger.info("All temporary directories deleted")

    @classmethod
    def setup_tmp_dirs(cls):
        """TODO
        """
        # Create main temporary directory
        cls._main_tmpdir_obj = TemporaryDirectory()
        cls._main_tmpdir = cls._main_tmpdir_obj.name
        cls.logger.info("Main temporary directory created: " + cls._main_tmpdir)
        # Create sandbox directory where the methods can write
        cls.sandbox_tmpdir = create_dir(
             os.path.join(cls._main_tmpdir, "sandbox"))
        cls.logger.info("Sandbox directory created: " + cls.sandbox_tmpdir)
        # Create a directory for data files (e.g. SQLite database) useful
        # for performing the tests
        cls.data_tmpdir = create_dir(os.path.join(cls._main_tmpdir, "data"))
        cls.logger.info("Data directory created: " + cls.data_tmpdir)

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
