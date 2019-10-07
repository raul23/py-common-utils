"""Module that defines tests for :mod:`~pyutils.dbutils`

Every functions in :mod:`~pyutils.dbutils` are tested here.

The command to execute the :mod:`unittest` test runner::

    python -m unittest discover

This command is executed at the root of the project directory .

"""

import os
import sqlite3
from tempfile import TemporaryDirectory
import unittest
# Custom modules
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
        # Create main temporary directory
        cls._main_tmpdir_obj = TemporaryDirectory()
        cls._main_tmpdir = cls._main_tmpdir_obj.name
        print("Main temporary directory created: ", cls._main_tmpdir)
        # Create sandbox directory where the methods can write
        cls.sanbox_tmpdir = create_dir(
            os.path.join(cls._main_tmpdir, "sandbox"))
        print("Sandbox directory created: ", cls.sanbox_tmpdir)
        # Create a directory for data files (e.g. YAML and txt files) useful
        # for performing the tests
        cls.datafiles_tmpdir = create_dir(
            os.path.join(cls._main_tmpdir, "datafiles"))
        print("Data files directory created: ", cls.datafiles_tmpdir)
        # Create SQLite db
        cls.db_filepath = os.path.join(cls.datafiles_tmpdir, "db.sqlite")
        create_db(cls.db_filepath, "tests/music.sql")

    @classmethod
    def tearDown(cls):
        """TODO

        """
        print("Cleanup...")
        # Cleanup temporary directory
        delete_folder_contents(cls._main_tmpdir)
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

    @unittest.skip("test_create_db_case_1()")
    def test_create_db_case_1(self):
        """Test that create_db() can create a SQLite database.

        """
        print("Testing case 1 of create_db()...")

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
