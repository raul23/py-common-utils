"""Module that defines tests for :mod:`~pyutils.dbutils`

Every functions in :mod:`~pyutils.dbutils` are tested here.

The command to execute the :mod:`unittest` test runner::

    python -m unittest discover

This command is executed at the root of the project directory .

"""

import os
import sqlite3
import unittest
# Custom modules
from .testutils import setup_tmp_dirs
from pyutils.genutils import create_dir, delete_folder_contents
from pyutils.dbutils import connect_db, create_db


class TestFunctions(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print()

    @classmethod
    def setUpClass(cls):
        """TODO

        """
        print("Setting up dbutils tests...")
        tmp_dirs = setup_tmp_dirs(with_sandbox=True, with_datafiles=True)
        cls._main_tmpdir_obj = tmp_dirs.main_tmpdir_obj
        cls._main_tmpdir = cls._main_tmpdir_obj.name
        cls.sandbox_tmpdir = tmp_dirs.sandbox_tmpdir
        cls.datafiles_tmpdir = tmp_dirs.datafiles_tmpdir
        cls.schema_filepath = "tests/music.sql"
        # Create SQLite db
        cls.db_filepath = os.path.join(cls.datafiles_tmpdir, "db.sqlite")
        create_db(cls.db_filepath, cls.schema_filepath)

    @classmethod
    def tearDown(cls):
        """TODO

        """
        print("Cleanup...")
        # Cleanup temporary directory
        delete_folder_contents(cls.sandbox_tmpdir)
        # print("Temporary directory cleared: ", cls.tmpdir)

    @classmethod
    def tearDownClass(cls):
        """TODO

        """
        print("\n\nFinal cleanup...")
        # Delete the temporary directory
        cls._main_tmpdir_obj.cleanup()
        print("Main temporary directory deleted: ", cls._main_tmpdir)

    # @unittest.skip("test_connect_db_case_1()")
    def test_connect_db_case_1(self):
        """Test that connect_db() can connect to a SQLite database.

        """
        print("Testing case 1 of connect_db()...")
        conn = connect_db(self.db_filepath)
        msg = "The returned connection is not an instance of sqlite3.Connection"
        self.assertIsInstance(conn, sqlite3.Connection, msg)
        print("Connection to SQLite database established")

    @unittest.skip("test_connect_db_case_2()")
    def test_connect_db_case_2(self):
        """Test connect_db() with autocommit=False.

        """
        print("Testing case 2 of connect_db()...")
        conn = connect_db(self.db_filepath)
        msg = "The returned connection is not an instance of sqlite3.Connection"
        self.assertIsInstance(conn, sqlite3.Connection, msg)
        print("Connection to SQLite database established")

    @unittest.skip("test_connect_db_case_3()")
    def test_connect_db_case_2(self):
        """Test connect_db() with autocommit=True.

        """
        print("Testing case 3 of connect_db()...")
        conn = connect_db(self.db_filepath)
        msg = "The returned connection is not an instance of sqlite3.Connection"
        self.assertIsInstance(conn, sqlite3.Connection, msg)
        print("Connection to SQLite database established")

    # @unittest.skip("test_create_db_case_1()")
    def test_create_db_case_1(self):
        """Test that create_db() can create a SQLite database.

        """
        print("Testing case 1 of create_db()...")
        db_filepath = os.path.join(self.sandbox_tmpdir, "db.sqlite")
        from pyutils.dbutils import logger
        with self.assertLogs(logger, 'INFO') as cm:
            retcode = create_db(db_filepath, self.schema_filepath)
        msg = "Log emitted not as expected"
        self.assertEqual(cm.output[-1], 'INFO:pyutils.dbutils:Database created!', msg)
        print("Log emitted as expected")
        msg = "The database couldn't be created. Return code is " \
              "{}".format(retcode)
        self.assertTrue(retcode == 0, msg)
        print("The database was created")

    @unittest.skip("test_create_db_case_2()")
    def test_create_db_case_2(self):
        """Test that create_db() can't overwrite a SQLite database when
        `overwrite_db` is set to False.

        """
        print("Testing case 2 of create_db()...")

    @unittest.skip("test_create_db_case_3()")
    def test_create_db_case_3(self):
        """Test that create_db() can overwrite a SQLite database when
        `overwrite_db` is set to True.

        """
        print("Testing case 3 of create_db()...")

    @unittest.skip("test_create_db_case_4()")
    def test_create_db_case_4(self):
        """Test that create_db() can't create a SQLite database when no schema
        is given.

        """
        print("Testing case 4 of create_db()...")


if __name__ == '__main__':
    unittest.main()
