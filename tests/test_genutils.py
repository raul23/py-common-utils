"""Module that defines tests for the module :mod:`~pyutils.genutils`

"""

import time
import unittest
# Custom modules
from pyutils.genutils import convert_utctime_to_local_tz, run_cmd


class TestFunctions(unittest.TestCase):

    @classmethod
    def setUp(cls):
        print()

    @classmethod
    def setUpClass(cls):
        print("Setting up genutils tests...\n")

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        print()

    def test_convert_utctime_to_local_tz_case_1(self):
        """Test case 1 for convert_utctime_to_local_tz()

        Case 1 consists in setting `utc_time` to a date and time which should be
        a :obj:`time.struct_time`. It then checks that the returned date and
        time is equal to the expected one in the local time zone.

        Notes
        -----
        `utc_time` is the argument given to :meth:`convert_utctime_to_local_tz`
        which will convert it into the local time zone.

        """
        print("Testing case 1 of convert_utctime_to_local_tz()...")
        # Case 1: utc_time is not None
        time_tuple = (2019, 10, 4, 6, 29, 19, 4, 277, 0)
        stime = time.struct_time(time_tuple)
        output = convert_utctime_to_local_tz(stime)
        # expected is the date and time given in the local time zone
        expected = '2019-10-04 02:29:19-04:00'
        msg = "Returned local datetime {} is different than expected " \
              "{}".format(output, expected)
        self.assertTrue(output == expected, msg)

    def test_convert_utctime_to_local_tz_case_2(self):
        """Test case 2 for convert_utctime_to_local_tz()

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
        regex = r"^\d{4}(-\d{2}){2} (\d{2}:){2}\d{2}-\d{2}:\d{2}$"
        self.assertRegex(output, regex)

    def test_create_directory(self):
        """Test create_directory()

        """
        print("\nTesting create_directory()...")

    def test_create_timestamped_dir(self):
        """Test create_timestamped_dir()

        """
        print("\nTesting create_timestamped_dir()...")

    def test_dumps_json(self):
        """Test dumps_json()

        """
        print("\nTesting dumps_json()...")

    def test_dumps_pickle(self):
        """Test dumps_pickle()

        """
        print("\nTesting dumps_pickle()...")

    def test_get_creation_date(self):
        """Test get_creation_date()

        """
        print("\nTesting get_creation_date()...")

    def test_load_json(self):
        """Test load_json()

        """
        print("\nTesting load_json()...")

    def test_load_pickle(self):
        """Test load_pickle()

        """
        print("\nTesting load_pickle()...")

    def test_load_yaml(self):
        """Test load_yaml()

        """
        print("\nTesting load_yaml()...")

    def test_read_file(self):
        """Test read_file()

        """
        print("\nTesting read_file()...")

    def test_read_yaml(self):
        """Test read_yaml()

        """
        print("\nTesting read_yaml()...")

    def test_run_cmd_date(self):
        """Test run_cmd() with the command ``date``

        """
        print("\nTesting run_cmd(cmd='date')...")
        self.assertTrue(run_cmd("date") == 0)

    def test_run_cmd_pwd(self):
        """Test run_cmd() with the command ``pwd``

        """
        print("\nTesting run_cmd(cmd='pwd')...")
        self.assertTrue(run_cmd("pwd") == 0)

    def test_write_file(self):
        """Test run_cmd()

        """
        print("\nTesting write_file()...")



if __name__ == '__main__':
    unittest.main()
