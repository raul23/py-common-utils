"""

"""

import os
from tempfile import TemporaryDirectory
# Custom modules
from pyutils.genutils import create_dir


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
