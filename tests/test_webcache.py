"""Module that defines tests for :mod:`~pyutils.webcache`

:class:`~pyutils.webcache.WebCache` and its methods are tested here.

"""

import os
import time
import unittest

from .utils import TestBase
from pyutils.webcache import WebCache


class TestFunctions(TestBase):
    # TODO
    test_name = "webcache"
    delay_between_requests = 2
    webcache = None
    cache_dirpath = None
    test_url = "https://en.wikipedia.org/wiki/Programming_language"

    @classmethod
    def setUpClass(cls):
        """TODO
        """
        super().setUpClass()
        # Create instance of WebCache by specifying the cache directory which
        # should be in the data temp directory
        cache_dirpath = os.path.join(cls.data_tmpdir, "webcache")
        cls.webcache = WebCache(delay_between_requests=cls.delay_between_requests,
                                cache_dirpath=cache_dirpath)
        # Cache the test webpage
        cls.webcache.cache_webpage(cls.test_url)
        # Since it is the first time the webpage is requested, it shouldn't
        # come from cache
        assert not cls.webcache.response.from_cache, \
            "The test webpage came from cache"
        print("Test webpage from cache: ", cls.webcache.response.from_cache)

    def get_webpage(self, url, test_from_cache=False):
        """TODO

        Parameters
        ----------
        url
        test_from_cache

        Returns
        -------

        """
        start = time.time()
        html = self.webcache.get_webpage(url)
        end = time.time()
        duration = end - start
        self.assertTrue(html, "HTML content is empty")
        if test_from_cache:
            msg = "The test webpage didn't come from cache"
            self.assertTrue(self.webcache.response.from_cache, msg)
            msg = "It took too long to get the webpage from cache"
            self.assertTrue(duration < 0.1, msg)
            print("The test webpage came from cache")
        else:
            msg = "The test webpage cam from cache"
            self.assertFalse(self.webcache.response.from_cache, msg)
            print("The test webpage was retrieved from a HTTP request")
            print("It took {} seconds to get the webpage".format(duration))

    # @unittest.skip("test_get_webpage_case_1()")
    def test_get_webpage_case_1(self):
        """Test that get_webpage() can successfully return a cached
        webpage.

        Case 1 consists in testing that
        :meth:`~pyutils.webcache.WebCache.get_webpage` retrieves the test
        webpage that was already cached. It asserts that it definitely came
        from cache and not retrieved through a HTTP request.

        """
        print("Testing case 1 of get_webpage()...")
        self.get_webpage(self.test_url, test_from_cache=True)

    # @unittest.skip("test_get_webpage_case_2()")
    def test_get_webpage_case_2(self):
        """Test that get_webpage() can retrieve a new webpage and cache
        it.

        Test 2 consists in testing that
        :meth:`~pyutils.webcache.WebCache.get_webpage` retrieves the test
        webpage that was already cached. It asserts that it definitely came
        from cache and not retrieved through a HTTP request.

        """
        print("\nTesting case 2 of get_webpage()...")
        new_url = "https://en.wikipedia.org/wiki/Algorithm"
        self.get_webpage(new_url, test_from_cache=False)


if __name__ == '__main__':
    unittest.main()
