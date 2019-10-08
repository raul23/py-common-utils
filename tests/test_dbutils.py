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
from pyutils.genutils import delete_folder_contents
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
        # Cleanup sandbox temporary directory ONLY
        # TODO: only sandbox directory is to be cleared
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

        TODO

        """
        # TODO
        print("\nTesting case 2 of connect_db()...")
        conn = connect_db(self.db_filepath)
        msg = "The returned connection is not an instance of sqlite3.Connection"
        self.assertIsInstance(conn, sqlite3.Connection, msg)
        print("Connection to SQLite database established")

    @unittest.skip("test_connect_db_case_3()")
    def test_connect_db_case_3(self):
        """Test connect_db() with autocommit=True.

        TODO

        """
        # TODO
        print("\nTesting case 3 of connect_db()...")
        conn = connect_db(self.db_filepath)
        msg = "The returned connection is not an instance of sqlite3.Connection"
        self.assertIsInstance(conn, sqlite3.Connection, msg)
        print("Connection to SQLite database established")

    # @unittest.skip("test_create_db_case_1()")
    def test_create_db_case_1(self):
        """Test that create_db() can create a SQLite database.

        This function tests that :meth:`~pyutils.dbutils.create_db` can create a
        SQLite database when valid arguments are given.

        At the same time, this function checks also the last message logged
        by :meth:~pyutils.dbutils.create_db`after the database was created.

        TODO: same time I am testing the dbutils' logger

        """
        print("\nTesting case 1 of create_db()...")
        db_filepath = os.path.join(self.sandbox_tmpdir, "db.sqlite")
        from pyutils.dbutils import logger
        with self.assertLogs(logger, 'INFO') as cm:
            retcode = create_db(db_filepath, self.schema_filepath)
        msg = "Log emitted not as expected"
        self.assertEqual(cm.output[-1],
                         'INFO:pyutils.dbutils:Database created!',
                         msg)
        print("Log emitted as expected")
        msg = "The database couldn't be created. Return code is " \
              "{}".format(retcode)
        self.assertTrue(retcode == 0, msg)
        print("The database was created")

    def overwrite_test_db(self, overwrite_db):
        """Create a test database and try to overwrite it.

        This function tests that :meth:`~pyutils.dbutils.create_db` that if
        `overwrite_db` is True, the test database will be overwritten.
        Otherwise, the database will not be overwritten.

        This function asserts two things:

        - the test database is created and
        - the validity of the return code obtained after trying to overwrite
        the test database.

        Parameters
        ----------
        overwrite_db : bool, optional
            Whether the test database will be overwritten.

        Notes
        -----
        This function is used by :meth:`test_create_db_case_2` and
        :meth:`test_create_db_case_3:.

        """
        db_filepath = os.path.join(self.sandbox_tmpdir, "db.sqlite")
        retcode1 = create_db(db_filepath, self.schema_filepath)
        msg = "The test database couldn't be created"
        self.assertTrue(retcode1 == 0, msg)
        retcode2 = create_db(db_filepath,
                             self.schema_filepath,
                             overwrite_db=overwrite_db,
                             pause=0)
        msg = "The option 'overwrite_db' didn't have any effect when " \
              "creating the database"
        expected = 0 if overwrite_db else 1
        self.assertTrue(retcode2 == expected, msg)

    # @unittest.skip("test_create_db_case_2()")
    def test_create_db_case_2(self):
        """Test that create_db() can't overwrite a SQLite database when
        `overwrite_db` is set to False.

        This function tests that :meth:`~pyutils.dbutils.create_db` can't
        overwrite a database that already exists on disk if `overwrite_db` is
        False.

        """
        print("\nTesting case 2 of create_db()...")
        self.overwrite_test_db(overwrite_db=False)
        print("The database wasn't overwritten")

    # @unittest.skip("test_create_db_case_3()")
    def test_create_db_case_3(self):
        """Test that create_db() can overwrite a SQLite database when
        `overwrite_db` is set to True.

        This function tests that :meth:`~pyutils.dbutils.create_db` can
        overwrite a database that already exists on disk if `overwrite_db` is
        True.

        """
        print("\nTesting case 3 of create_db()...")
        self.overwrite_test_db(overwrite_db=True)
        print("The database was overwritten")

    # @unittest.skip("test_create_db_case_4()")
    def test_create_db_case_4(self):
        """Test that create_db() raises an exception when a non-existing schema
        is given.

        This function tests that :meth:`~pyutils.dbutils.create_db` raises an
        IOError when the path of the schema doesn't exist.

        """
        print("\nTesting case 4 of create_db()...")
        db_filepath = os.path.join(self.sandbox_tmpdir, "db.sqlite")
        with self.assertRaises(IOError) as cm:
            create_db(db_filepath, self.schema_filepath+'_bad')
        print("The database couldn't be created because no schema was given")
        print("Raised an IOError as expected: ", cm.exception)

    # @unittest.skip("test_create_db_case_5()")
    def test_create_db_case_5(self):
        """Test that create_db() raises an exception when a faulty database
        path is given.

        This function tests that :meth:`~pyutils.dbutils.create_db` raises an
        IOError when the path of the database is wrong.

        """
        print("\nTesting case 5 of create_db()...")
        with self.assertRaises(sqlite3.OperationalError) as cm:
            create_db("/bad/db/path/db.sqlite", self.schema_filepath)
        print("The database couldn't be created because a wrong db path was "
              "given")
        print("Raised an sqlite3.OperationalError as expected: ", cm.exception)


if __name__ == '__main__':
    unittest.main()
