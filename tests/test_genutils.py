"""Module that defines tests for :mod:`~pyutils.genutils`

The command to execute the :mod:`unittest` test runner::

    python -m unittest discover

This command is executed at the root of the project directory or in ``tests/``.

"""

from datetime import datetime
import os
import shutil
from tempfile import TemporaryDirectory
import time
import unittest
# Third-party modules
import tzlocal
# Custom modules
from pyutils.genutils import convert_utctime_to_local_tz, create_directory, \
    create_timestamped_dir, delete_folder_contents, run_cmd, write_file


class TestFunctions(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print()

    @classmethod
    def setUpClass(cls):
        """TODO

        """
        print("Setting up genutils tests...")
        # Create main temporary directory
        cls.main_tmpdir_obj = TemporaryDirectory()
        cls.main_tmpdir = cls.main_tmpdir_obj.name
        print("Main temporary directory created: ", cls.main_tmpdir)
        # Create sandbox directory where the methods can write
        cls.sanbox_tmpdir = create_directory(
            os.path.join(cls.main_tmpdir, "sandbox"))
        print("Sandbox directory created: ", cls.sanbox_tmpdir)
        # Create a directory for data files (e.g. YAML and txt files) useful
        # for performing the tests
        cls.datafiles_tmpdir = create_directory(
            os.path.join(cls.main_tmpdir, "datafiles"))
        print("Data files directory created: ", cls.datafiles_tmpdir)

    @classmethod
    def tearDown(cls):
        """TODO

        """
        print("Cleanup...")
        # Cleanup sandbox directory
        delete_folder_contents(cls.sanbox_tmpdir)
        # print("Sandbox directory cleared: ", cls.sanbox_tmpdir)

    @classmethod
    def tearDownClass(cls):
        """TODO

        """
        print("\n\nFinal cleanup...")
        cls.main_tmpdir_obj.cleanup()
        print("Main temporary directory deleted: ", cls.main_tmpdir_obj.name)

    def test_convert_utctime_to_local_tz_case_1(self):
        """Test convert_utctime_to_local_tz() returns a valid time.

        Case 1 consists in checking that the returned date and time is equal
        to the expected one in the local time zone.

        Notes
        -----
        `utc_time` is the argument given to :meth:`convert_utctime_to_local_tz`
        which will convert it into the local time zone.

        The function sets `utc_time` to a date and time which is a
        :obj:`time.struct_time`

        """
        print("Testing case 1 of convert_utctime_to_local_tz()...")
        # Case 1: utc_time is not None
        time_tuple = (2019, 10, 4, 6, 29, 19, 5, 277, 0)
        stime = time.struct_time(time_tuple)
        output = convert_utctime_to_local_tz(stime)
        # TODO: explain
        if tzlocal.get_localzone().zone == 'UTC':
            # tzlocal couldn't find any timezone configuration and thus
            # defaulted to UTC
            expected = '2019-10-04 06:29:19+00:00'
            msg = "Returned local datetime {} is different than expected " \
                  "{}".format(output, expected)
            self.assertTrue(output == expected, msg)
        else:
            expected = '2019-10-04 ??:29:19???:00'
            exp1 = output[0:11] == expected[0:11]
            exp2 = output[13:19] == expected[13:19]
            msg = "UTC time '{}' was incorrectly converted into the local time " \
                  "as '{}'".format(str(datetime(*stime[:7])), output)
            self.assertTrue(exp1 and exp2, msg)

    def test_convert_utctime_to_local_tz_case_2(self):
        """Test convert_utctime_to_local_tz() when no UTC time is given.

        Case 2 consists in setting `utc_time` to None and checking that the
        returned date and time follows the pattern::

            YYYY-MM-DD HH:MM:SS-HH:MM

        Notes
        -----
        `utc_time` is the argument given to :meth:`convert_utctime_to_local_tz`
        which will convert it into the local time zone.

        """
        print("\nTesting case 2 of convert_utctime_to_local_tz()...")
        # Case 2: utc_time is None
        # By default, if no argument is given, utc_time is None
        output = convert_utctime_to_local_tz()
        # This regex only checks that the digits composing the date and time
        # are in the good order without checking that each digit is in the
        # correct range of numbers, e.g. the first digit for month should be in
        # the ange [0,1] and so on. The regex would be too complex. The current
        # regex already does a good job.
        # E.g. (0[1-9]|1[0-2])-((0[1-9])|([1-2][0-9])|(3[0-1])) matches any
        # MM-DD where the MM can take values in [01-12] and DD in [01-31]
        regex = r"^\d{4}(-\d{2}){2} (\d{2}:){2}\d{2}[-|+]\d{2}:\d{2}$"
        self.assertRegex(output, regex)

    def test_create_directory_case_1(self):
        """Test that create_directory() actually creates a directory.

        Case 1 consists in testing that the directory was actually created on
        disk.

        """
        print("\nTesting case 1 of create_directory()...")
        dirpath = os.path.join(self.sanbox_tmpdir, "testdir")
        msg = "The directory {} couldn't be created".format(dirpath)
        try:
            create_directory(dirpath)
        except (FileExistsError, PermissionError) as e:
            self.fail("{} : {}".format(msg, e))
        else:
            self.assertTrue(os.path.isdir(dirpath), msg)
            print("The directory was created")

    def test_create_directory_case_2(self):
        """Test create_directory() when the directory already exists.

        Case 2 consists in checking that the function :meth:`create_directory`
        raises a :exc:`FileExistsError` when we try to create a directory that
        already exists on disk.

        """
        print("\nTesting case 2 of create_directory() ...")
        with self.assertRaises(FileExistsError):
            dirpath = os.path.join(self.sanbox_tmpdir, "testdir")
            create_directory(dirpath)
            create_directory(dirpath)
        print("Raised a FileExistsError exception as expected")

    def test_create_directory_case_3(self):
        """Test create_directory() with no permission to write in a directory.

        Case 3 consists in checking that the function :meth:`create_directory`
        raises a :exc:`PermissionError` when we try to create a subdirectory in
        a directory without the write permission.

        """
        print("\nTesting case 3 of create_directory() ...")
        test1_dirpath = os.path.join(self.sanbox_tmpdir, "testdir1")
        create_directory(test1_dirpath)
        # TODO: Only works on macOS/Linux:
        os.chmod(test1_dirpath, 0o444)
        with self.assertRaises(PermissionError):
            test2_dirpath = os.path.join(test1_dirpath, "testdir2")
            create_directory(test2_dirpath)
        print("Raised a PermissionError exception as expected")
        # Put back write permission to owner
        os.chmod(test1_dirpath, 0o744)

    # @unittest.skip("test_create_timestamped_dir_case_1()")
    def test_create_timestamped_dir_case_1(self):
        """Test that create_timestamped_dir() actually creates a timestamped
        directory without suffix.

        Case 1 consists in testing that the timestamped directory without
        suffix in its name was actually created on disk by calling
        :meth:`os.path.isdir` on the directory path.

        Notes
        -----
        It is trickier to test the case where
        :meth:`create_create_timestamped_directory` must raise a
        :exc:`FileExistsError` exception since you can't easily create a
        timestamped directory that already exists, unless for example you call
        :meth:`create_create_timestamped_directory` twice very quickly and the
        second call might rise a :exc:`FileExistsError` exception if it ends up
        using an already taken timestamped directory name (with the seconds and
        all).

        """
        print("\nTesting case 1 of create_timestamped_dir()...")
        msg = "The timestamped directory couldn't be created"
        try:
            dirpath = create_timestamped_dir(self.sanbox_tmpdir)
        except (FileExistsError, PermissionError) as e:
            self.fail("{} : {}".format(msg, e))
        else:
            self.assertTrue(os.path.isdir(dirpath), msg)
            print("The timestamped directory was created")

    # @unittest.skip("test_create_timestamped_dir_case_2()")
    def test_create_timestamped_dir_case_2(self):
        """Test create_timestamped_dir() with no permission to write in a
        directory.

        Case 2 consists in checking that the function
        :meth:`create_create_timestamped_directory` raises a
        :exc:`PermissionError` when we try to create a subdirectory in a
        directory without the write permission.

        """
        print("\nTesting case 2 of create_timestamped_dir() ...")
        test1_dirpath = os.path.join(self.sanbox_tmpdir, "testdir1")
        create_directory(test1_dirpath)
        # TODO: Only works on macOS/Linux:
        os.chmod(test1_dirpath, 0o444)
        with self.assertRaises(PermissionError):
            test2_dirpath = os.path.join(test1_dirpath, "testdir2")
            create_timestamped_dir(test2_dirpath)
        print("Raised a PermissionError exception as expected")
        # Put back write permission to owner
        os.chmod(test1_dirpath, 0o744)

    def create_text_files(self, dirpath, text="Hello World!\n", number_files=2):
        """Create text files in a directory.

        `number_files` text files are created in the directory `dirpath` with
        the text `text`.

        Parameters
        ----------
        dirpath : str
            Path to the directory where the text files are created.
        number_files : int, optional
            Number of files to create in the directory (the default value is 2).

        """
        for i in range(1, number_files + 1):
            filepath = os.path.join(dirpath, "file{}.txt".format(i))
            write_file(filepath, text)

    def populate_folder(self, number_subdirs=2, number_files=2):
        """Populate a folder with text files and subdirectories.

        This function is to be used when testing
        :meth:`~genutils.delete_folder_contents`, see
        :meth:`test_delete_folder_contents_case_1` and
        :meth:`test_delete_folder_contents_case_2`.

        It creates a main test directory with `number_files` text files, and
        `number_subdirs` subdirectories with each storing `number_files` text
        files.

        Parameters
        ----------
        number_files : int, optional
            Number of files to create per subdirectory (the default value is 2).
        number_subdirs : int, optional
            Number of subdirectories to create (the default value is 2).

        Returns
        -------
        main_test_dirpath : str
            Path to the main directory which stores the subdirectories along
            with their text files.

        """
        # TODO: add symbolic links
        # Create a main test directory where many subdirectories with text
        # files will be created
        maintest_dirpath = os.path.join(self.sanbox_tmpdir, "main_testdir")
        create_directory(maintest_dirpath)
        self.create_text_files(dirpath=maintest_dirpath,
                          text="Hello, World!\nI will be deleted soon :(\n",
                          number_files=number_files)
        for i in range(1, number_subdirs+1):
            # Create the subdirectories with text files
            test_dirpath = os.path.join(maintest_dirpath, "testdir{}".format(i))
            create_directory(test_dirpath)
            self.create_text_files(dirpath=test_dirpath,
                              text="Hello, World!\nI will be deleted soon :(\n",
                              number_files=number_files)
        return maintest_dirpath

    # @unittest.skip("test_delete_folder_contents_case_1()")
    def test_delete_folder_contents_case_1(self):
        """Test that delete_folder_contents() removes everything in a folder.

        Case 1 consists in testing that :meth:`delete_folder_contents` removes
        everything in a folder, including the files and subdirectories at the
        root of the given folder.

        See Also
        --------
        populate_folder : populates a folder with text files and subdirectories.

        Notes
        -----
        Case 1 sets `remove_subdirs` to True and `delete_recursively` to False.

        """
        print("\nTesting case 1 of delete_folder_contents()...")
        # Create the main test directory along with subdirectories and files
        dirpath = self.populate_folder()
        # Delete the whole content of the main test directory
        delete_folder_contents(dirpath)
        # Test that the folder is empty
        msg = "The folder {} couldn't be cleared".format(dirpath)
        self.assertTrue(len(os.listdir(dirpath)) == 0, msg)
        print("The folder {} is empty".format(dirpath))

    # @unittest.skip("test_delete_folder_contents_case_2()")
    def test_delete_folder_contents_case_2(self):
        """Test that delete_folder_contents() removes everything at the root
        of a directory except subdirectories and their contents.

        Case 2 consists in testing that :meth:`delete_folder_contents` removes
        everything in a folder, except the subdirectories and their contents at
        the root of the given folder.

        See Also
        --------
        populate_folder : populates a folder with text files and subdirectories.

        Notes
        -----
        Case 2 sets `remove_subdirs` to False and `delete_recursively` to False.

        """
        print("\nTesting case 2 of delete_folder_contents()...")
        # Create the main test directory along with subdirectories and files
        dirpath = self.populate_folder()
        # Delete everything in the main test directory, except subdirectories
        # and their contents
        delete_folder_contents(dirpath, remove_subdirs=False)
        # Test that the folder only has subdirectories but no files at its root
        for root, dirs, files in os.walk(dirpath):
            if root == dirpath:
                msg = "There is a file at the top of the directory"
                self.assertTrue(len(files) == 0, msg)
            else:
                msg = "There is a subdirectory that is empty"
                self.assertTrue(len(files) > 0, msg)
        print("No files found at the top and the subdirectories are not "
              "empty".format(dirpath))

    # @unittest.skip("test_delete_folder_contents_case_3()")
    def test_delete_folder_contents_case_3(self):
        """Test that delete_folder_contents() removes all text files
        recursively, except subdirectories.

        Case 3 consists in testing that :meth:`delete_folder_contents` removes
        all text files recursively, except subdirectories. Thus, at the end,
        anything left should be subdirectories, including the root directory.

        See Also
        --------
        populate_folder : populates a folder with text files and subdirectories.

        Notes
        -----
        Case 3 sets `remove_subdirs` to False and `delete_recursively` to True.

        """
        print("\nTesting case 3 of delete_folder_contents()...")
        # Create the main test directory along with subdirectories and files
        dirpath = self.populate_folder()
        # Delete all text files recursively in the main test directory, except
        # subdirectories
        delete_folder_contents(folderpath=dirpath,
                               remove_subdirs=False,
                               delete_recursively=True)
        # Test that only the subdirectories are left
        for root, dirs, files in os.walk(dirpath):
            msg = "There is a file"
            self.assertTrue(len(files) == 0, msg)
        print("All subdirectories are empty including the main "
              "directory".format(dirpath))

    @unittest.skip("test_delete_folder_contents_case_4()")
    def test_delete_folder_contents_case_4(self):
        """Test that delete_folder_contents() removes everything at the root
        of a directory except subdirectories and their contents.

        Remove everything recursively at the root
        remove_subdirs=True and delete_recursively=True

        Case 4 consists in testing that :meth:`delete_folder_contents` removes
        everything in a folder, except the subdirectories and their contents at
        the root of the given folder.

        See Also
        --------
        populate_folder : populates a folder with text files and subdirectories.

        Notes
        -----
        Case 2 sets `remove_subdirs` to True and `delete_recursively` to True.

        """
        print("\nTesting case 4 of delete_folder_contents()...")
        import ipdb
        ipdb.set_trace()
        # Create the main test directory along with subdirectories and files
        dirpath = self.populate_folder()
        # Delete everything in the main test directory, except subdirectories
        delete_folder_contents(folderpath=dirpath,
                               remove_subdirs=False,
                               delete_recursively=True)

    @unittest.skip("test_dumps_json()")
    def test_dumps_json(self):
        """Test dumps_json()

        """
        print("\nTesting dumps_json()...")

    @unittest.skip("test_dumps_pickle()")
    def test_dumps_pickle(self):
        """Test dumps_pickle()

        """
        print("\nTesting dumps_pickle()...")

    @unittest.skip("test_get_creation_date()")
    def test_get_creation_date(self):
        """Test get_creation_date()

        """
        print("\nTesting get_creation_date()...")

    @unittest.skip("test_load_json()")
    def test_load_json(self):
        """Test load_json()

        """
        print("\nTesting load_json()...")

    @unittest.skip("test_load_pickle()")
    def test_load_pickle(self):
        """Test load_pickle()

        """
        print("\nTesting load_pickle()...")

    @unittest.skip("test_dumps_pickle()")
    def test_load_yaml(self):
        """Test load_yaml()

        """
        print("\nTesting load_yaml()...")

    @unittest.skip("test_read_file()")
    def test_read_file(self):
        """Test read_file()

        """
        print("\nTesting read_file()...")

    @unittest.skip("test_read_yaml()")
    def test_read_yaml(self):
        """Test read_yaml()

        """
        print("\nTesting read_yaml()...")

    @unittest.skip("test_run_cmd_date()")
    def test_run_cmd_date(self):
        """Test run_cmd() with the command ``date``

        """
        print("\nTesting run_cmd(cmd='date')...")
        print("Command output: ")
        self.assertTrue(run_cmd("date") == 0)

    @unittest.skip("test_run_cmd_pwd()")
    def test_run_cmd_pwd(self):
        """Test run_cmd() with the command ``pwd``

        """
        print("\nTesting run_cmd(cmd='pwd')...")
        print("Command output: ")
        self.assertTrue(run_cmd("pwd") == 0)

    @unittest.skip("test_write_file()")
    def test_write_file(self):
        """Test run_cmd()

        """
        print("\nTesting write_file()...")


if __name__ == '__main__':
    unittest.main()
