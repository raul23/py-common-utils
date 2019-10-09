"""Module that defines a class for caching webpages on disk.

TODO: is it true?
Only the HTML content of the webpage is cached on disk, thus the other
resources, such as pictures, might not get rendered when viewed on a
browser.

.. _HTTP request header:
   https://www.webopedia.com/TERM/H/HTTP_request_header.html
.. _List of all HTTP headers (Mozilla):
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
.. _List of HTTP header fields (Wikipedia):
   https://en.wikipedia.org/wiki/List_of_HTTP_header_fields

"""

import logging
import os
import sys
import time
from logging import NullHandler

try:
    import requests
    import requests_cache
except ImportError as e:
    raise ImportError("{} not found. You can install it with: pip "
                      "install {}".format(e.name, e.name))

from pyutils.exceptions import HTTP404Error
from pyutils.genutils import create_dir
from pyutils.logging_wrapper import LoggingWrapper


# Setup default logging with handler that does nothing
logging.getLogger(__name__).addHandler(NullHandler())


class WebCache:
    """A class that caches webpages on disk.

    TODO: is it true?
    The HTML content of the webpages is cached on disk. Thus, other resources
    (such as pictures) might not get rendered when viewed on a browser.

    When retrieving webpages, a certain delay is introduced between HTTP
    requests to the server in order to reduce its workload.

    Parameters
    ----------
    http_get_timeout : int, optional
        Timeout when a **GET** request doesn't receive any response from the
        server. After the timeout expires, the **GET** request is dropped (the
        default value is 5 seconds).
    delay_between_requests : int, optional
        A delay will be added between HTTP requests in order to reduce the
        workload on the server (the default value is 8 seconds which implies
        that there will be a delay of 8 seconds between successive HTTP
        requests).
    headers : dict, optional
        The information added to the **HTTP GET** request that a user's browser
        sends to a Web server containing the details of what the browser wants
        and will accept back from the server. See `HTTP request header`_ (the
        default value is defined in :attr:`~SaveWebpages.headers`).

        Its keys are the request headers' field names like `Accept`, `Cookie`,
        `User-Agent`, or `Referer` and its values are the associated request
        headers' field values. *See* `List of all HTTP headers (Mozilla)`_ *and*
        `List of HTTP header fields (Wikipedia)`_.
    expire_after : int, optional
        TODO: add this option in the main config

    """

    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/44.0.2403.157 "
                             "Safari/537.36c",
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,"
                         "image/webp,*/*;q=0.8"}
    """
    The information added to the **HTTP GET** request that a user's browser 
    sends to a Web server containing the details of what the browser wants and 
    will accept back from the server.
    """
    _cache_name = "cache"
    """
    TODO
    """
    _cache_dirpath = "~/.cache/pyutils_webcache"
    """
    TODO
    """

    def __init__(self, http_get_timeout=5, delay_between_requests=8,
                 headers=headers, expire_after=300,
                 cache_dirpath=_cache_dirpath):
        self.http_get_timeout = http_get_timeout
        self.delay_between_requests = delay_between_requests
        self.headers = headers
        self.expire_after = expire_after
        self._cache_dirpath = os.path.expanduser(cache_dirpath)
        self.logger = logging.getLogger(__name__)
        # Experimental option: add color to log messages
        if os.environ.get('COLOR_LOGS'):
            self.logger = LoggingWrapper(self.logger,
                                         os.environ.get('COLOR_LOGS'))
        # Setup cache
        self._cache_filename = os.path.join(self._cache_dirpath, "cache")
        self._setup_cache()
        self.cache = requests_cache.get_cache()
        # Establish a session to be used for the GET requests
        # IMPORTANT: the session must be established after installing the cache
        # if you want all your responses to be cached, i.e. monkey-patching
        # requests. Ref.: https://bit.ly/2MCDCeD
        self._req_session = requests.Session()
        # Add headers to the request session
        self._req_session.headers = self.headers
        self._last_request_time = -sys.float_info.max
        self.response = None

    def _setup_cache(self):
        """TODO
        """
        try:
            # Create cache directory
            create_dir(self._cache_dirpath)
        except FileExistsError:
            self.logger.debug("Cache directory already exists: "
                              "{}".format(self._cache_dirpath))
        except PermissionError as e:
            self.logger.exception(e)
            self.logger.warning("The cache directory couldn't be created!")
            # TODO: abort program or follow with no cache?
            raise
        else:
            self.logger.info("Cache directory created: "
                             "{}".format(self._cache_dirpath))
        # Install cache
        requests_cache.install_cache(self._cache_filename,
                                     backend='sqlite',
                                     expire_after=self.expire_after)

    def cache_webpage(self, url):
        """TODO

        Parameters
        ----------
        url

        Returns
        -------

        Raises
        ------

        """
        try:
            _ = self.get_webpage(url)
        except (requests.exceptions.RequestException, HTTP404Error):
            raise

    def get_webpage(self, url):
        """Get the HTMl content of a webpage.

        When retrieving the webpage, a certain delay is introduced between HTTP
        requests to the server in order to reduce the workload on the server.

        Parameters
        ----------
        url : str
            URL of the webpage whose HTML content will be retrieved.

        Raises
        ------
        HTTP404Error
            Raised if the server returns a 404 status code because the webpage
            is not found.
        requests.RequestException
            Raised if there is a :mod:`requests`-related error, e.g.
            :exc:`requests.ConnectionError` if the URL is not known.

        Returns
        -------
        TODO: html

        """
        if self.cache.has_url(url):
            self.logger.debug("The URL was found in cache. Webpage will be "
                              "retrieved from cache.")
            response = self._req_session.get(url)
        else:
            # Add in function
            # TODO: explain delay computations
            current_delay = time.time() - self._last_request_time
            diff_between_delays = \
                current_delay - self.delay_between_requests
            if diff_between_delays < 0:
                self.logger.debug("Waiting {} seconds before sending next HTTP "
                                  "request...".format(abs(diff_between_delays)))
                time.sleep(abs(diff_between_delays))
                self.logger.debug("Time is up! HTTP request will be sent.")
            self._last_request_time = time.time()
            try:
                response = self._send_request(url)
            except requests.exceptions.RequestException:
                raise

        self.response = response
        html = response.text
        if response.status_code == 404:
            raise HTTP404Error(
                "404: PAGE NOT FOUND. The URL '{}' returned a 404 status "
                "code.".format(url))
        elif response.status_code == 200:
            self.logger.debug("200: OK. Webpage successfully retrieved!")
        else:
            self.logger.debug(
                "Request response: status code is {}".format(
                    response.status_code))
        return html

    def _send_request(self, url):
        """TODO

        Parameters
        ----------
        url

        Returns
        -------

        """
        try:
            self.logger.debug("Sending HTTP request ...")
            response = self._req_session.get(url, timeout=self.http_get_timeout)
        except requests.exceptions.RequestException:
            raise
        else:
            return response
