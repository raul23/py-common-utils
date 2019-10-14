"""Module that defines tests for :mod:`~pyutils.dbutils`

Every functions in :mod:`~pyutils.dbutils` are tested here.

"""

import os
import sqlite3

import unittest

import pyutils.dbutils as dbutils
from .utils import TestBase
from pyutils.dbutils import connect_db, create_db


class TestFunctions(TestBase):
    # TODO
    test_module_name = "dbutils"
    CREATE_TEST_DATABASE = True

    # @unittest.skip("test_connect_db_case_1()")
    def test_connect_db_case_1(self):
        """Test that connect_db() can connect to a SQLite database.
        """
        self.logger.info("Testing <color>case 1 of connect_db()</color>...")
        conn = connect_db(self.db_filepath)
        msg = "The returned connection is not an instance of sqlite3.Connection"
        self.assertIsInstance(conn, sqlite3.Connection, msg)
        self.logger.info("Connection to SQLite database established")

    @unittest.skip("test_connect_db_case_2()")
    def test_connect_db_case_2(self):
        """Test connect_db() with autocommit=False.
        TODO
        """
        self.logger.info("\nTesting <color>case 2 of connect_db()</color>...")
        conn = connect_db(self.db_filepath)
        msg = "The returned connection is not an instance of sqlite3.Connection"
        self.assertIsInstance(conn, sqlite3.Connection, msg)
        self.logger.info("Connection to SQLite database established")

    @unittest.skip("test_connect_db_case_3()")
    def test_connect_db_case_3(self):
        """Test connect_db() with autocommit=True.
        TODO
        """
        # TODO
        self.logger.info("\nTesting <color>case 3 of connect_db()</color>...")
        conn = connect_db(self.db_filepath)
        msg = "The returned connection is not an instance of sqlite3.Connection"
        self.assertIsInstance(conn, sqlite3.Connection, msg)
        self.logger.info("Connection to SQLite database established")

    # @unittest.skip("test_create_db_case_1()")
    def test_create_db_case_1(self):
        """Test that create_db() can create a SQLite database.

        This function tests that :meth:`~pyutils.dbutils.create_db` can create a
        SQLite database when valid arguments are given.

        At the same time, this function checks also the last message logged
        by :meth:~pyutils.dbutils.create_db`after the database was created.

        """
        self.logger.info("\nTesting <color>case 1 of create_db()</color>...")
        db_filepath = os.path.join(self.sandbox_tmpdir, "db.sqlite")
        retcode = self.assert_logs(
            logger=dbutils.logger,
            level="INFO",
            str_to_find="Database created!",
            fnc=create_db,
            db_filepath=db_filepath,
            schema_filepath=self.schema_filepath
        )
        msg = "The database couldn't be created. Return code is " \
              "{}".format(retcode)
        self.assertTrue(retcode == 0, msg)
        self.logger.info("The database was created")

    # @unittest.skip("test_create_db_case_2()")
    def test_create_db_case_2(self):
        """Test that create_db() can't overwrite a SQLite database when
        `overwrite_db` is set to False.

        This function tests that :meth:`~pyutils.dbutils.create_db` can't
        overwrite a database that already exists on disk if `overwrite_db` is
        False.

        """
        self.logger.info("\nTesting <color>case 2 of create_db()</color>...")
        self.overwrite_test_db(overwrite_db=False)
        self.logger.info("The database wasn't overwritten as expected")

    # @unittest.skip("test_create_db_case_3()")
    def test_create_db_case_3(self):
        """Test that create_db() can overwrite a SQLite database when
        `overwrite_db` is set to True.

        This function tests that :meth:`~pyutils.dbutils.create_db` can
        overwrite a database that already exists on disk if `overwrite_db` is
        True.

        """
        self.logger.info("\nTesting <color>case 3 of create_db()</color>...")
        self.overwrite_test_db(overwrite_db=True)
        self.logger.info("The database was overwritten as expected")

    # @unittest.skip("test_create_db_case_4()")
    def test_create_db_case_4(self):
        """Test that create_db() raises an exception when a non-existing schema
        is given. TODO: not raising an exception anymore, but asserting logs

        This function tests that :meth:`~pyutils.dbutils.create_db` raises an
        IOError when the path of the schema doesn't exist.

        """
        self.logger.info("\nTesting <color>case 4 of create_db()</color>...")
        db_filepath = os.path.join(self.sandbox_tmpdir, "db.sqlite")
        retcode = self.assert_logs(
            logger=dbutils.logger,
            level="ERROR",
            str_to_find="FileNotFoundError",
            fnc=create_db,
            db_filepath=db_filepath,
            schema_filepath='/bad/schema/path.sql'
        )
        msg = "Unexpected return code: {}".format(retcode)
        self.assertTrue(retcode == 1, msg)
        self.logger.info("As expected, the database couldn't be created "
                         "because no schema was given")

    # @unittest.skip("test_create_db_case_5()")
    def test_create_db_case_5(self):
        """Test that create_db() raises an exception when a faulty database
        path is given. TODO: not raising an exception anymore, but asserting logs

        This function tests that :meth:`~pyutils.dbutils.create_db` raises an
        IOError when the path of the database is wrong.

        """
        self.logger.info("\nTesting <color>case 5 of create_db()</color>...")
        retcode = self.assert_logs(
            logger=dbutils.logger,
            level="ERROR",
            str_to_find="OperationalError",
            fnc=create_db,
            db_filepath="/bad/db/path.sqlite",
            schema_filepath=self.schema_filepath
        )
        msg = "Unexpected return code: {}".format(retcode)
        self.assertTrue(retcode == 1, msg)
        self.logger.info("As expected, the database couldn't be created "
                         "because a wrong db path was given")

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


if __name__ == '__main__':
    unittest.main()
