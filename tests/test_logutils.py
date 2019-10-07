"""Module that defines tests for :mod:`~pyutils.logutils`

Every functions in :mod:`~pyutils.logutils` are tested here.

The command to execute the :mod:`unittest` test runner::

    python -m unittest discover

This command is executed at the root of the project directory or in ``tests/``.

"""

from tempfile import TemporaryDirectory
import unittest
# Custom modules
from pyutils.genutils import delete_folder_contents


class TestFunctions(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print()

    @classmethod
    def setUpClass(cls):
        """TODO

        """
        print("Setting up genutils tests...")
        # Create temporary directory
        cls.tmpdir_obj = TemporaryDirectory()
        cls.tmpdir = cls.tmpdir_obj.name
        print("Temporary directory created: ", cls.tmpdir)

    @classmethod
    def tearDown(cls):
        """TODO

        """
        print("Cleanup...")
        # Cleanup temporary directory
        delete_folder_contents(cls.tmpdir)
        # print("Temporary directory cleared: ", cls.tmpdir)

    @classmethod
    def tearDownClass(cls):
        """TODO

        """
        print("\n\nFinal cleanup...")
        # Delete the temporary directory
        cls.tmpdir_obj.cleanup()
        print("Temporary directory deleted: ", cls.tmpdir)


if __name__ == '__main__':
    unittest.main()
