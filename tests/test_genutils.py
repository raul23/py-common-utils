"""Module that defines tests for :mod:`~pyutils.genutils`

Every functions in :mod:`~pyutils.genutils` is tested here.

The command to execute the :mod:`unittest` test runner::

    python -m unittest discover

This command is executed at the root of the project directory or in ``tests/``.

"""

from datetime import datetime
import os
from tempfile import TemporaryDirectory
import time
import unittest
# Third-party modules
import tzlocal
import yaml
# Custom modules
from pyutils.genutils import convert_utctime_to_local_tz, create_dir, \
    create_timestamped_dir, delete_folder_contents, dumps_json, dump_pickle, \
    get_creation_date, load_json, load_pickle, load_yaml, read_file, run_cmd, \
    write_file


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

    def test_convert_utctime_to_local_tz_case_1(self):
        """Test that convert_utctime_to_local_tz() returns a valid time.

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

        Case 2 consists setting `utc_time` to None and testing that
        :meth:`convert_utctime_to_local_tz` returns a date and time that
        follows the pattern::

            YYYY-MM-DD HH:MM:SS-HH:MM

        Notes
        -----
        When `utc_time` is None, :meth:`convert_utctime_to_local_tz` will use
        UTC as the timezone for the current time.

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

    def test_create_dir_case_1(self):
        """Test that create_dir() actually creates a directory.

        Case 1 consists in testing that the directory was actually created on
        disk by the function :meth:`create_dir()`.

        """
        print("\nTesting case 1 of create_dir()...")
        dirpath = os.path.join(self.tmpdir, "testdir")
        msg = "The directory {} couldn't be created".format(dirpath)
        try:
            create_dir(dirpath)
        except (FileExistsError, PermissionError) as e:
            self.fail("{} : {}".format(msg, e))
        else:
            self.assertTrue(os.path.isdir(dirpath), msg)
            print("The directory was created")

    def test_create_dir_case_2(self):
        """Test create_dir() when the directory already exists.

        Case 2 consists in checking that the function :meth:`create_dir`
        raises a :exc:`FileExistsError` when we try to create a directory that
        already exists on disk.

        """
        print("\nTesting case 2 of create_dir() ...")
        with self.assertRaises(FileExistsError):
            dirpath = os.path.join(self.tmpdir, "testdir")
            create_dir(dirpath)
            create_dir(dirpath)
        print("Raised a FileExistsError exception as expected")

    def test_create_dir_case_3(self):
        """Test create_dir() with no permission to write in a directory.

        Case 3 consists in checking that the function :meth:`create_dir`
        raises a :exc:`PermissionError` when we try to create a subdirectory in
        a directory without the write permission.

        """
        print("\nTesting case 3 of create_dir() ...")
        test1_dirpath = os.path.join(self.tmpdir, "testdir1")
        create_dir(test1_dirpath)
        # TODO: Only works on macOS/Linux:
        os.chmod(test1_dirpath, 0o444)
        with self.assertRaises(PermissionError):
            create_dir(os.path.join(test1_dirpath, "testdir2"))
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
            dirpath = create_timestamped_dir(self.tmpdir)
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
        test1_dirpath = os.path.join(self.tmpdir, "testdir1")
        create_dir(test1_dirpath)
        # TODO: Only works on macOS/Linux:
        os.chmod(test1_dirpath, 0o444)
        with self.assertRaises(PermissionError):
            create_timestamped_dir(os.path.join(test1_dirpath, "testdir2"))
        print("Raised a PermissionError exception as expected")
        # Put back write permission to owner
        os.chmod(test1_dirpath, 0o744)

    def create_text_files(self, dirpath, text="Hello World!\n", number_files=2):
        """Create text files in a directory.

        `number_files` text files are created in the directory `dirpath` with
        the text `text`.

        Parameters
        ----------
        text : str
            Text to write in each file.
        dirpath : str
            Path to the directory where the text files are created.
        number_files : int, optional
            Number of files to create in the directory (the default value is 2).

        """
        for i in range(1, number_files + 1):
            write_file(os.path.join(dirpath, "file{}.txt".format(i)), text)

    def populate_folder(self, number_subdirs=2, number_files=2):
        """Populate a folder with text files and subdirectories.

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

        Notes
        -----
        This function is to be used when testing
        :meth:`~genutils.delete_folder_contents`, see
        :meth:`test_delete_folder_contents_case_1` and
        :meth:`test_delete_folder_contents_case_2`.

        """
        # TODO: add symbolic links
        # Create a main test directory where many subdirectories with text
        # files will be created
        maintest_dirpath = os.path.join(self.tmpdir, "main_testdir")
        create_dir(maintest_dirpath)
        self.create_text_files(
            dirpath=maintest_dirpath,
            text="Hello, World!\nI will be deleted soon :(\n",
            number_files=number_files)
        for i in range(1, number_subdirs+1):
            # Create the subdirectories with text files
            test_dirpath = os.path.join(maintest_dirpath, "testdir{}".format(i))
            create_dir(test_dirpath)
            self.create_text_files(
                dirpath=test_dirpath,
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
        # Test that the main test directory is empty
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
            msg = "There is still a file in the main test directory"
            self.assertTrue(len(files) == 0, msg)
        print("All subdirectories are empty including the main "
              "directory".format(dirpath))

    # @unittest.skip("test_delete_folder_contents_case_4()")
    def test_delete_folder_contents_case_4(self):
        """Test that delete_folder_contents() removes everything in a folder
        with `delete_recursively` set to True.

        Case 4 consists in testing that :meth:`delete_folder_contents` removes
        everything in a folder with the flag `delete_recursively` set to False.

        See Also
        --------
        populate_folder : populates a folder with text files and subdirectories.

        Notes
        -----
        Case 4 sets `remove_subdirs` to True and `delete_recursively` to True.
        Case 4 is similar to case 1 where everything is deleted but with
        `remove_subdirs` set to True and `delete_recursively` to False.

        """
        print("\nTesting case 4 of delete_folder_contents()...")
        # Create the main test directory along with subdirectories and files
        dirpath = self.populate_folder()
        # Delete everything recursively in the main test directory
        delete_folder_contents(folderpath=dirpath,
                               remove_subdirs=True,
                               delete_recursively=True)
        # Test that the main test directory is empty
        msg = "The folder {} couldn't be cleared".format(dirpath)
        self.assertTrue(len(os.listdir(dirpath)) == 0, msg)
        print("The folder {} is empty".format(dirpath))

    # @unittest.skip("test_delete_folder_contents_case_5()")
    def test_delete_folder_contents_case_5(self):
        """Test delete_folder_contents() when a folder doesn't exist.

        Case 5 consists in testing that :meth:`delete_folder_contents` raises
        an :exc:`OSError` exception when the folder to be cleared doesn't exist.

        See Also
        --------
        populate_folder : populates a folder with text files and subdirectories.

        """
        print("\nTesting case 5 of delete_folder_contents()...")
        try:
            # Delete everything in the directory that doesn't exist
            delete_folder_contents(
                folderpath=os.path.join(self.tmpdir, "fakedir"),
                remove_subdirs=True,
                delete_recursively=False)
        except OSError:
            print("Raised an OSError exception as expected")
        else:
            self.fail("An OSError exception was not raised as expected")

    # @unittest.skip("test_dump_and_load_pickle()")
    def test_dump_and_load_pickle(self):
        """Test that dump_pickle() writes and load data correctly to/from a
        file on disk.

        This function tests that the data saved on disk is not corrupted by
        loading it and checking that it is the same as the original data.

        Thus, :meth:`dump_pickle` and :meth:`load_pickle` are tested at the
        same time.

        """
        print("\nTesting dump_pickle()...")
        data1 = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': {
                'key3-1': 'value3-1',
                'key3-2': 'value3-2'
            }
        }
        filepath = os.path.join(self.tmpdir, "data.pkl")
        dump_pickle(filepath, data1)
        # Test that the data was correctly written by loading it
        data2 = load_pickle(filepath)
        msg = "The data that was saved on disk is corrupted"
        self.assertDictEqual(data1, data2, msg)
        print("The data was pickled and saved correctly")

    # @unittest.skip("test_dumps_and_load_json_case_1()")
    def test_dumps_and_load_json_case_1(self):
        """Test that dumps_json() writes and loads data correctly to/from a JSON
        file with its keys sorted.

        Case 1 tests that the JSON data saved on disk is not corrupted by
        loading it and checking that it is the same as the original JSON data
        and that its keys are sorted.

        Thus, :meth:`dumps_json` and :meth:`load_json` are tested at the same
        time.

        """
        print("\nTesting case 1 of dumps_json()...")
        data1 = {
            'key1': 'value1',
            'key3': {
                'key3-2': 'value3-2',
                'key3-1': 'value3-1'
            },
            'key2': 'value2'
        }
        filepath = os.path.join(self.tmpdir, "data.json")
        dumps_json(filepath, data1)
        # Test that the JSON data was correctly written by loading it
        data2 = load_json(filepath)
        msg = "The JSON data that was saved on disk is corrupted"
        self.assertDictEqual(data1, data2, msg)
        # Test that the keys from the JSON data are sorted
        # NOTE: Only the keys at level 1 of the JSON dict are tested
        self.assertSequenceEqual(sorted(data1.keys()), list(data2.keys()))
        print("The JSON data was saved correctly with its keys sorted")

    # @unittest.skip("test_dumps_and_load_json_case_2()")
    def test_dumps_and_load_json_case_2(self):
        """Test that dumps_json() writes and loads data correctly to/from a JSON
        file with its keys not sorted.

        Case 2 tests that the JSON data saved on disk is not corrupted by
        loading it and checking that it is the same as the original JSON data
        and that its keys are not sorted.

        Thus, :meth:`dumps_json` and :meth:`load_json` are tested at the same
        time.

        """
        print("\nTesting case 2 of dumps_json()...")
        data1 = {
            'key1': 'value1',
            'key3': {
                'key3-2': 'value3-2',
                'key3-1': 'value3-1'
            },
            'key2': 'value2'
        }
        filepath = os.path.join(self.tmpdir, "data.json")
        dumps_json(filepath, data1, sort_keys=False)
        # Test that the JSON data was correctly written by loading it
        data2 = load_json(filepath)
        msg = "The JSON data that was saved on disk is corrupted"
        self.assertDictEqual(data1, data2, msg)
        # Test that the keys from the JSON data are not sorted
        # NOTE: Only the keys at level 1 of the JSON dict are tested
        self.assertSequenceEqual(list(data1.keys()), list(data2.keys()))
        print("The JSON data was saved correctly with its keys not sorted")

    # @unittest.skip("test_get_creation_date()")
    def test_get_creation_date(self):
        """Test that get_creation_date() returns a valid creation date for a
        file.

        This function tests :meth:`get_creation_date` by comparing the creation
        date of a file and the current date and time.

        """
        print("\nTesting get_creation_date()...")
        # Write file to disk
        filepath = os.path.join(self.tmpdir, "file.txt")
        write_file(filepath, "Hello, World!\n")
        # Get the current time
        now = str(datetime.fromtimestamp(time.time()))
        # Get the file creation date
        creation = str(datetime.fromtimestamp(get_creation_date(filepath)))
        # Compare the two times to an accuracy of a decasecond (10s).
        # NOTE: However, we could test to an accuracy of a second but it is
        # better to be safe.
        msg = "File creation date ('{}') not as expected " \
              "('{}')".format(creation, now)
        self.assertTrue(now[:19] == creation[:19], msg)
        print("Current time: ", now)
        print("Valid file creation date: ", creation)

    # @unittest.skip("test_load_yaml()")
    def test_load_yaml(self):
        """Test that load_yaml() loads data correctly from a YAML file.

        This function tests that :meth:`load_yaml` can load a YAML data from a
        file on disk by checking that it is the same as the original data.

        """
        print("\nTesting load_yaml()...")
        # Write YAML data to a file on disk
        data1 = {
            'key1': 'value1',
            'key3': {
                'key3-2': 'value3-2',
                'key3-1': 'value3-1'
            },
            'key2': 'value2'
        }
        filepath = os.path.join(self.tmpdir, "file.yaml")
        with open(filepath, 'w') as f:
            yaml.dump(data1, f, default_flow_style=False, sort_keys=False)
        # Test that the YAML data was correctly written by loading it
        data2 = load_yaml(filepath)
        msg = "The YAML data that was saved on disk is corrupted"
        self.assertDictEqual(data1, data2, msg)
        print("The YAML data was saved correctly")

    # @unittest.skip("test_read_file_case_1()")
    def test_read_file_case_1(self):
        """Test that read_file() reads a file on disk.

        Case 1 consists in checking that :meth:`read_file()` can read a text
        file from disk by checking that its content is the same as the
        original data.

        """
        print("\nTesting case 1 of read_file()...")
        # Write text to a file on disk
        text1 = "Hello World!\n"
        filepath = os.path.join(self.tmpdir, "file.txt")
        write_file(filepath, text1)
        # Test that the text was correctly written by loading it
        text2 = read_file(filepath)
        msg = "The text that was saved on disk is corrupted"
        self.assertTrue(text1==text2, msg)
        print("The text was saved correctly")

    # @unittest.skip("test_read_file_case_2()")
    def test_read_file_case_2(self):
        """Test that read_file() when a file doesn't exist.

        Case 2 consists in checking that :meth:`read_file()` raises an
        :exc:`OSError` exception when a file doesn't exist.

        """
        print("\nTesting case 2 of read_file()...")
        # Write text to a file on disk
        with self.assertRaises(OSError):
            read_file(os.path.join(self.tmpdir, "file.txt"))
        print("Raised an OSError exception as expected")

    # @unittest.skip("test_run_cmd_date()")
    def test_run_cmd_date(self):
        """Test run_cmd() with the command ``date``

        """
        print("\nTesting run_cmd(cmd='date')...")
        print("Command output: ")
        self.assertTrue(run_cmd("date") == 0)

    # @unittest.skip("test_run_cmd_pwd()")
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
