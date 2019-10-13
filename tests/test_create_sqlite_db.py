"""Module that defines tests for :mod:`~pyutils.scripts.create_sqlite_db`

The script ``create_sqlite_db.py`` is tested here with different combinations of
command-line options.

"""

import os
import sqlite3
import sys
import unittest
# Custom modules
from .utils import TestBase
from pyutils.scripts import create_sqlite_db


class TestFunctions(TestBase):
    # TODO
    test_name = "create_sqlite_db"
    CREATE_TEST_DATABASE = True

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
                    '-s', self.schema_filepath]
        retcode = create_sqlite_db.main()
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
                    '-d', self.db_filepath,
                    '-s', self.schema_filepath,
                    '-p', 0]
        retcode = create_sqlite_db.main()
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
                    '-d', self.db_filepath,
                    '-s', self.schema_filepath,
                    '-p', 0]
        retcode = create_sqlite_db.main()
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
                    '-d', self.db_filepath,
                    '-s', '/bad/schema/path.sql',
                    '-p', 0]
        with self.assertRaises(IOError) as cm:
            create_sqlite_db.main()
        print("Raised an IOError as expected:", cm.exception)

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
                    '-s', self.schema_filepath]
        with self.assertRaises(sqlite3.OperationalError) as cm:
            create_sqlite_db.main()
        print("Raised a sqlite3.OperationalError as expected:", cm.exception)


if __name__ == '__main__':
    unittest.main()
