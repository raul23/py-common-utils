"""Module that defines tests for :mod:`~pyutils.genutils`

"""

from datetime import datetime
import os
from tempfile import TemporaryDirectory
import time
import unittest
# Third-party modules
import tzlocal
# Custom modules
from pyutils.genutils import convert_utctime_to_local_tz, create_directory, \
    delete_folder_contents, run_cmd
# import ipdb


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
        """Test case 1 of convert_utctime_to_local_tz()

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
            exp1 = output[0:11] == expected[0:13]
            exp2 = output[13:19] == expected[13:19]
            msg = "UTC time '{}' was incorrectly converted into the local time " \
                  "as '{}'".format(str(datetime(*stime[:7])), output)
            self.assertTrue(exp1 and exp2, msg)

    def test_convert_utctime_to_local_tz_case_2(self):
        """Test case 2 of convert_utctime_to_local_tz()

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
        """Test that create_directory() actually created a directory

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
            print("The directory could be created")

    def test_create_directory_case_2(self):
        """Test create_directory() when a directory already exists

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
        """Test create_directory() with no permission write in a directory

        Case 3 consists in checking that the function :meth:`create_directory`
        raises a :exc:`PermissionError` when we try to create a directory in a
        directory without the write permission.

        """
        print("\nTesting case 3 of create_directory() ...")
        testdir1_path = os.path.join(self.sanbox_tmpdir, "testdir1")
        create_directory(testdir1_path)
        # TODO: Only works on macOS/Linux:
        os.chmod(testdir1_path, 0o444)
        with self.assertRaises(PermissionError):
            testdir2_path = os.path.join(testdir1_path, "testdir2")
            create_directory(testdir2_path)
        print("Raised a PermissionError exception as expected")
        # Put back write permission to owner
        os.chmod(testdir1_path, 0o744)

    @unittest.skip("test_create_timestamped_dir()")
    def test_create_timestamped_dir(self):
        """Test create_timestamped_dir()

        """
        print("\nTesting create_timestamped_dir()...")

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
