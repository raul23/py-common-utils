"""TODO

"""

import os
from tempfile import TemporaryDirectory
import unittest
# Custom modules
from pyutils.genutils import create_dir
from pyutils.genutils import delete_folder_contents


class TestBase(unittest.TestCase):

    # TODO
    _main_tmpdir_obj = None
    _main_tmpdir = None
    sandbox_tmpdir = None
    data_tmpdir = None
    test_name = ""

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
        print("Main temporary directory deleted: ", cls._main_tmpdir)

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
        cls.data_tmpdir = create_dir(
            os.path.join(cls._main_tmpdir, "data"))
        print("Data directory created: ", cls.data_tmpdir)


def setup_tmp_dirs(with_sandbox=False, with_datafiles=False):
    """TODO

    Parameters
    ----------
    with_sandbox : bool, optional
    with_datafiles : bool, optional

    Returns
    -------

    """
    # Create main temporary directory
    main_tmpdir_obj = TemporaryDirectory()
    main_tmpdir = main_tmpdir_obj.name
    print("Main temporary directory created: ", main_tmpdir)
    sandbox_tmpdir = None
    datafiles_tmpdir = None
    if with_sandbox:
        # Create sandbox directory where the methods can write
        sandbox_tmpdir = create_dir(os.path.join(main_tmpdir, "sandbox"))
        print("Sandbox directory created: ", sandbox_tmpdir)
    if with_datafiles:
        # Create a directory for data files (e.g. SQLite database) useful for
        # performing the tests
        datafiles_tmpdir = create_dir(os.path.join(main_tmpdir, "datafiles"))
        print("Data files directory created: ", datafiles_tmpdir)

    class TmpDirs:
        """TODO

        """
        @classmethod
        def setupClass(cls):
            cls.main_tmpdir_obj = main_tmpdir_obj
            cls.sandbox_tmpdir = sandbox_tmpdir
            cls.datafiles_tmpdir = datafiles_tmpdir

    TmpDirs.setupClass()
    return TmpDirs
