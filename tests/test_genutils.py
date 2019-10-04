"""Module that ...

"""

import re
import time
import unittest
# Custom modules
from pyutils.genutils import convert_utctime_to_local_tz


class TestFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up genutils tests...\n")

    def test_convert_utctime_to_local_tz(self):
        """Test convert_utctime_to_local_tz()

        Notes
        -----
        :meth:`~genutils.convert_utctime_to_local_tz` converts a given UTC time
        into the local time zone.

        """
        print("Testing ")
        # Test case 1: utc_time is not None
        time_tuple = (2019, 10, 4, 6, 29, 19, 4, 277, 0)
        stime = time.struct_time(time_tuple)
        output = convert_utctime_to_local_tz(stime)
        expected = '2019-10-04 02:29:19-04:00'
        msg = "Returned local datetime {} is different than expected " \
              "{}".format(output, expected)
        self.assertTrue(output == expected, msg)
        # Test case 2: utc_time is None
        # By default, if no argument is given, utc_time is None
        output = convert_utctime_to_local_tz()
        # self.assertRegex(output, )


if __name__ == '__main__':
    unittest.main()
