"""Module that defines tests for :mod:`~pyutils.scripts.create_sqlite_db`

The command to execute the :mod:`unittest` test runner::

    python -m unittest discover

This command is executed at the root of the project directory.

"""

import os
import sqlite3
import sys
import unittest
# Custom modules
from .utils import TestBase
from pyutils.dbutils import create_db
from pyutils.scripts import create_sqlite_db
from pyutils.scripts.create_sqlite_db import main


class TestFunctions(TestBase):
    # TODO
    test_name = "create_sqlite_db"
    _schema_filepath = "tests/music.sql"
    _db_filepath = None

    @classmethod
    def setUpClass(cls):
        """TODO: overrides

        """
        super().setUpClass()
        # Create SQLite db
        cls._db_filepath = os.path.join(cls.data_tmpdir, "db.sqlite")
        create_db(cls._db_filepath, cls._schema_filepath)

    # @unittest.skip("test_main_case_1()")
    def test_main_case_1(self):
        """Test that main() can create a SQLite database when the right paths
        are provided.

        Case 1 tests that :meth:`~pyutils.scripts.create_sqlite_db.main()` can
        create a SQLite database by providing paths to the database and schema
        in the command-line.

        """
        print("Testing case 1 of main()...")
        db_filepath = os.path.join(self.sandbox_tmpdir, "db.sqlite")
        sys.argv = ['create_sqlite_db.py', '-o',
                    '-d', db_filepath,
                    '-s', self._schema_filepath]
        retcode = main()
        msg = "The database couldn't be created. Return code is " \
              "{}".format(retcode)
        self.assertTrue(retcode == 0, msg)
        print("The database was created")

    # @unittest.skip("test_main_case_2()")
    def test_main_case_2(self):
        """Test that main() can't overwrite a database when the option -o is
        not used.

        Case 2 tests that :meth:`~pyutils.scripts.create_sqlite_db.main()` can't
        overwrite a SQLite database when the option `-o` is not used in the
        command-line.

        """
        print("\nTesting case 2 of main()...")
        sys.argv = ['create_sqlite_db.py',
                    '-d', self._db_filepath,
                    '-s', self._schema_filepath]
        create_sqlite_db.PAUSE = 0
        retcode = main()
        msg = "Something very odd! Return code is {}".format(retcode)
        self.assertTrue(retcode == 1, msg)
        print("The database wasn't overwritten as expected")

    # @unittest.skip("test_main_case_3()")
    def test_main_case_3(self):
        """Test that main() can overwrite a database when the option -o is used.

        Case 3 tests that :meth:`~pyutils.scripts.create_sqlite_db.main()` can
        overwrite a SQLite database when the option `-o` is used in the
        command-line.

        """
        print("\nTesting case 3 of main()...")
        sys.argv = ['create_sqlite_db.py', '-o',
                    '-d', self._db_filepath,
                    '-s', self._schema_filepath]
        create_sqlite_db.PAUSE = 0
        retcode = main()
        msg = "Something very odd! Return code is {}".format(retcode)
        self.assertTrue(retcode == 0, msg)
        print("The database was overwritten as expected")

    # @unittest.skip("test_main_case_4()")
    def test_main_case_4(self):
        """Test that main() can't create a database when a schema that doesn't
        exist is given.

        Case 4 tests that :meth:`~pyutils.scripts.create_sqlite_db.main()` raises
        an :exc:`IOError` when a schema that doesn't exist is given in the
        command-line.

        """
        print("\nTesting case 4 of main()...")
        sys.argv = ['create_sqlite_db.py', '-o',
                    '-d', self._db_filepath,
                    '-s', '/bad/schema/path.sql']
        with self.assertRaises(IOError) as cm:
            main()
        print("Raised an IOError as expected: ", cm.exception)

    # @unittest.skip("test_main_case_5()")
    def test_main_case_5(self):
        """Test that main() can't create a database when a database path that
        doesn't exist is given.

        Case 5 tests that :meth:`~pyutils.scripts.create_sqlite_db.main()`
        raises a :exc:`sqlite3.OperationalError` when a database path that
        doesn't exist is given in the command-line.

        """
        print("\nTesting case 5 of main()...")
        sys.argv = ['create_sqlite_db.py', '-o',
                    '-d', '/bad/db/path.sqlite',
                    '-s', self._schema_filepath]
        with self.assertRaises(sqlite3.OperationalError) as cm:
            main()
        print("Raised a sqlite3.OperationalError as expected: ", cm.exception)


if __name__ == '__main__':
    unittest.main()
