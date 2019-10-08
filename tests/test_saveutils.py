"""Module that defines tests for :mod:`~pyutils.saveutils`

:class:`~pyutils.saveutils.SaveWebpages` and its methods are tested here.

"""

import unittest
# Custom modules
from .utils import TestBase


class TestFunctions(TestBase):
    test_name = "saveutils"

    # @unittest.skip("test_get_cached_webpage_case_1()")
    def test_get_cached_webpage_case_1(self):
        """Test that get_cached_webpage() can successfully return a cached
        webpage.

        Case 1 consists in testing that
        :meth:`~pyutils.saveutils.SaveWebpages.get_cached_webpage` can
        successfully return a cached webpage by comparing it with the
        original one (hash values are compared).

        """
        print("Testing case 1 of get_cached_webpage()...")


if __name__ == '__main__':
    unittest.main()
