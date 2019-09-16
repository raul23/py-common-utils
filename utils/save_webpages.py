"""Module that defines a class for saving webpages on disk.

Only the HTML content of the webpage is saved on disk, thus the other resources,
such as pictures, might not get rendered when viewed on a browser.

"""

import logging
import os
import sys
import time
from logging import NullHandler
# Third-party modules
import requests
# Custom modules
import utils.exceptions.files as files_exc
import utils.exceptions.connection as connec_exc
from utils.genutils import read_file, write_file
from utils.logging.logging_wrapper import LoggingWrapper


# Setup logging
logging.getLogger(__name__).addHandler(NullHandler())


class SaveWebpages:
    """A class that saves webpages on disk.

    The HTML content of the webpages are saved on disk. Thus, other resources
    (such as pictures) might not get rendered when viewed on a browser.

    When retrieving webpages, a certain delay is introduced between HTTP
    requests to the server in order to reduce its workload.

    Parameters
    ----------
    overwrite_webpages : bool, optional
        Whether a webpage that is saved on disk can be overwritten (the default
        value is True which implies that the webpages can be overwritten on
        disk).
    http_get_timeout : int, optional
        Timeout when a GET request doesn't receive any response from the server.
        After the timeout expires, the GET request is dropped (the default
        value is 5 seconds).
    headers : dict, optional
        The information added to the HTTP GET request that a user's browser
        sends to a Web server containing the details of what the browser wants
        and will accept back from the server [1] (the default value is defined
        below).

        Its keys are the request headers' field names like `Accept`, `Cookie`,
        `User-Agent`, or `Referer` and its values are the associated request
        headers' field values [2][3].

    Methods
    -------
    get_cached_webpage()
        Load a webpage from disk.
    save_webpage()
        Save a webpage on disk.
    get_webpage()
        Get the HTMl content of a webpage.

    References
    ----------
    .. [1] `HTTP request header <https://bit.ly/2lOMrIv/>`_.
    .. [2] `List of all HTTP headers (Mozilla) <https://mzl.la/2QuSKev>`_.
    .. [3] `List of HTTP header fields (Wikipedia) <https://bit.ly/2qMmXbI>`_.

    """

    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/44.0.2403.157 "
                             "Safari/537.36c",
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,"
                         "image/webp,*/*;q=0.8"}

    def __init__(self, overwrite_webpages=False, http_get_timeout=5,
                 delay_between_requests=8, headers=headers):
        self.overwrite_webpages = overwrite_webpages
        self.http_get_timeout = http_get_timeout
        self.delay_between_requests = delay_between_requests
        self.headers = headers
        self.logger = logging.getLogger(__name__)
        # Experimental option: add color to log messages
        if os.environ.get('COLOR_LOGS'):
            self.logger = LoggingWrapper(self.logger,
                                         os.environ.get('COLOR_LOGS'))
        # Establish a session to be used for the GET requests
        self.req_session = requests.Session()
        self.last_request_time = -sys.float_info.max

    def get_cached_webpage(self, filepath):
        """Load a webpage from disk.

        Load the HTML content of a webpage from disk.

        The webpages are cached in order to reduce the number of requests to the
        server.

        Parameters
        ----------
        filepath : str
            The file path of the webpage to load from disk.

        Raises
        ------
        OSError
            Raised if an I/O related error occurs while reading the cached HTML
            document, e.g. the file doesn't exist.

        Returns
        -------
        html : str
            HTML content of the webpage that is loaded from disk.

        """
        try:
            self.logger.debug(
                "Reading the cached HTML file '{}'".format(filepath))
            html = read_file(filepath)
        except OSError as e:
            raise OSError(e)
        else:
            self.logger.debug(
                "The webpage HTML was successfully loaded from '{}'".format(
                    filepath))
            return html

    def save_webpage(self, filepath, url):
        """Save a webpage on disk.

        First, the webpage is checked if it's already cached. If it's found in
        cache, then its HTML content is simply returned.

        If the webpage is not found in cache, then it's retrieved from the
        server and saved on disk.

        IMPORTANT: the webpage found on cache might also be overwritten if the
        option `overwrite_webpages` is set to True.

        Parameters
        ----------
        filepath : str
            File path of the webpage that will be saved on disk.
        url : str
            URL to the webpage that will be saved on disk.

        Raises
        ------
        HTTP404Error
            Raised if the server returns a 404 status code because the webpage
            is not found.
        OverwriteFileError
            Raised if an existing file is being overwritten and the flag to
            overwrite files is disabled.
        OSError
            Raised if an I/O related error occurs while writing the webpage on
            disk, e.g. the file doesn't exist.

        Returns
        -------
        html : str
            HTML content of the webpage that is saved on disk.

        """
        try:
            if os.path.isfile(filepath) and not self.overwrite_webpages:
                html = self.get_cached_webpage(filepath)
            else:
                # Retrieve webpage
                html = self.get_webpage(url)
                self.logger.debug("Webpage retrieved!")
                # Write webpage locally
                self.logger.debug(
                    "Saving webpage to '{}'".format(filepath))
                write_file(filepath, html, self.overwrite_webpages)
                self.logger.debug("The webpage is saved in '{}'. URL is "
                                  "'{}'".format(filepath, url))
        except (connec_exc.HTTP404Error,
                files_exc.OverwriteFileError,
                OSError) as e:
            # HTTP404Error from _get_webpage()
            # OverwriteFileError  from write_file()
            # OSError from _get_webpage() and write_file()
            raise e
        return html

    def get_webpage(self, url):
        """Get the HTMl content of a webpage.

        When retrieving the webpage, a certain delay is introduced between HTTP
        requests to the server in order to reduce its workload.

        Parameters
        ----------
        url : str
            URL of the webpage whose HTML content will be retrieved.

        Raises
        ------
        HTTP404Error
            Raised if the server returns a 404 status code because the webpage
            is not found.
        RequestException
            Raised if there is a `requests`-related error, e.g. ConnectionError
            if the URL is not known. A lot of `requests` error are derived from
            OSError, e.g. ConnectionError, HTTPError, SSLError

        Returns
        -------
        html : str
            HTML content of the webpage that is saved on disk.

        """
        current_delay = time.time() - self.last_request_time
        diff_between_delays = \
            current_delay - self.delay_between_requests
        if diff_between_delays < 0:
            self.logger.debug("Waiting {} seconds before sending next HTTP "
                              "request...".format(abs(diff_between_delays)))
            time.sleep(abs(diff_between_delays))
            self.logger.debug("Time is up! HTTP request will be sent.")
        try:
            self.logger.debug("Sending HTTP request ...")
            self.last_request_time = time.time()
            req = self.req_session.get(
                url,
                headers=self.headers,
                timeout=self.http_get_timeout)
            html = req.text
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(e)
        else:
            if req.status_code == 404:
                raise connec_exc.HTTP404Error(
                    "404: PAGE NOT FOUND. The URL '{}' returned a 404 status "
                    "code.".format(url))
            elif req.status_code == 200:
                self.logger.debug("200: OK. Webpage successfully retrieved!")
            else:
                self.logger.debug(
                    "Request response: status code is {}".format(req.status_code))
        return html
