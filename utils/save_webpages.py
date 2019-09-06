"""Module that defines a class for saving webpages on disk.

Only the HTML content of the webpage is saved on disk, thus the other resources,
such as pictures, might not get rendered when viewed on a browser.

"""

from datetime import datetime
import os
import requests
import sys
import time
# Custom modules
import utils.exceptions.files as files_exc
import utils.exceptions.connection as connec_exc
from utils.genutils import read_file, write_file
from utils.databases.dbutils import get_logger


class SaveWebpages:
    """A class that saves webpages on disk.

    The HTML content of the webpages are saved on disk. Thus, other resources
    (such as pictures) might not get rendered when viewed on a browser.

    When retrieving webpages, a certain delay is introduced between HTTP
    requests to the server in order to reduce its workload.

    Parameters
    ----------
    main_cfg : dict
        Configuration ``dict`` that contains the necessary options for
        configuring HTTP requests. For more information about these options,
        check the content of this
        `configuration file <https://bit.ly/2lGbeOw/>`_.
    logger : dict or LoggingWrapper
        The logger can be setup through a logging configuration ``dict``. If a
        logger of type ``LoggingWrapper`` is passed, it implies that a logger
        is already setup.

    """

    def __init__(self, main_cfg, logger):
        self.main_cfg = main_cfg
        self.http_get_timeout = main_cfg['http_get_timeout']
        self.delay_between_requests = main_cfg['delay_between_requests']
        self.headers = main_cfg['headers']
        self.logger = get_logger(__name__,
                                 __file__,
                                 os.getcwd(),
                                 logger)
        # Establish a session to be used for the GET requests
        self.req_session = requests.Session()
        self.last_request_time = -sys.float_info.max

    def load_cached_webpage(self, filepath):
        """Load a webpage from disk.

        Load the HTML content of a webpage from disk and also retrieve the date
        and time the page was first accessed.

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
        webpage_accessed : datetime.datetime
            The date and time the webpage was accessed the first time, e.g.
            `datetime.datetime(2019, 8, 20, 17, 52, 13)`.

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
            # Get the file's modified as the datetime the webpage was
            # originally accessed
            webpage_accessed = \
                datetime.fromtimestamp(os.path.getmtime(filepath))
            return html, webpage_accessed

    def save_webpage(self, filepath, url, overwrite_webpages=True):
        """Save a webpage on disk.

        First, the webpage is checked if it's already cached. If it's found in
        cache, then its HTML content is simply returned.

        The webpages are cached in order to reduce the number of requests to the
        server.

        Parameters
        ----------
        filepath : str
            File path of the webpage that will be saved on disk.
        url : str
            URL to the webpage that will be saved on disk.
        overwrite_webpages : bool, optional
            Whether a webpage that is saved on disk can be overwritten (by
            default the value is True which implies that the webpages can be
            overwritten on disk).

        Raises
        ------
        HTTP404Error
            Raised if the server returns a 404 status code because the webpage
            is not found.
        OverwriteFileError
            Raised if an existing file is being overwritten and the flag to
            allow to overwrite is disabled.
        OSError
            Raised if an I/O related error occurs while writing the webpage on
            disk, e.g. the file doesn't exist.

        Returns
        -------
        html : str
            HTML content of the webpage that is saved on disk.
        webpage_accessed : datetime.datetime
            The date and time the webpage was accessed the first time, e.g.
            `datetime.datetime(2019, 8, 20, 17, 52, 13)`.

        """
        try:
            if os.path.isfile(filepath) and not overwrite_webpages:
                html, webpage_accessed = self.load_cached_webpage(filepath)
            else:
                # Retrieve webpage and the datetime the webpage was first
                # accessed
                html = self._get_webpage(url)
                self.logger.debug("Webpage retrieved!")
                # Write webpage locally
                self.logger.debug(
                    "Saving webpage to '{}'".format(filepath))
                write_file(filepath, html, overwrite_webpages)
                # Get the file's modified as the datetime the webpage was
                # originally accessed
                # TODO: test modification datetime
                webpage_accessed = \
                    datetime.fromtimestamp(os.path.getmtime(filepath))
                self.logger.debug("The webpage is saved in '{}'. URL is "
                                  "'{}'".format(filepath, url))
        except (connec_exc.HTTP404Error,
                files_exc.OverwriteFileError,
                OSError) as e:
            # HTTP404Error from _get_webpage()
            # OverwriteFileError  from write_file()
            # OSError from _get_webpage() and write_file()
            raise e
        return html, webpage_accessed

    def _get_webpage(self, url):
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
                    "404 - PAGE NOT FOUND. The URL '{}' returned a 404 status "
                    "code.".format(url))
        return html
