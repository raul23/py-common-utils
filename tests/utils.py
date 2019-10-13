"""TODO

"""

import os
from tempfile import TemporaryDirectory
import unittest

from .data.logging import logging_cfg_dict
from pyutils.dbutils import create_db
from pyutils.genutils import create_dir, delete_folder_contents


class TestBase(unittest.TestCase):
    # TODO
    test_name = "TestBase"
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
        # TODO: fix long print
        print("\n# ========================================================="
              "==================================== #")
        print("                                     {}".format(cls.test_name))
        print("# ========================================================="
              "==================================== #")
        print("Setting up {} tests...".format(cls.test_name))
        cls.setup_tmp_dirs()
        if cls.CREATE_TEST_DATABASE:
            # Create SQLite db
            cls.db_filepath = os.path.join(cls.data_tmpdir, "db.sqlite")
            create_db(cls.db_filepath, cls.schema_filepath)
            print("SQLite database created: ", cls.db_filepath)

    @classmethod
    def tearDown(cls):
        """TODO
        """
        print("Cleanup...")
        # Cleanup temporary directories
        # TODO: explain the if...
        if cls.sandbox_tmpdir:
            delete_folder_contents(cls.sandbox_tmpdir)

    @classmethod
    def tearDownClass(cls):
        """TODO
        """
        print("\n\nFinal cleanup...")
        # Delete the temporary directory
        cls._main_tmpdir_obj.cleanup()
        print("All temporary directories deleted")

    @classmethod
    def setup_tmp_dirs(cls):
        """TODO
        """
        # Create main temporary directory
        cls._main_tmpdir_obj = TemporaryDirectory()
        cls._main_tmpdir = cls._main_tmpdir_obj.name
        print("Main temporary directory created: ", cls._main_tmpdir)
        # Create sandbox directory where the methods can write
        cls.sandbox_tmpdir = create_dir(
             os.path.join(cls._main_tmpdir, "sandbox"))
        print("Sandbox directory created: ", cls.sandbox_tmpdir)
        # Create a directory for data files (e.g. SQLite database) useful
        # for performing the tests
        cls.data_tmpdir = create_dir(os.path.join(cls._main_tmpdir, "data"))
        print("Data directory created: ", cls.data_tmpdir)
