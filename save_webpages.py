"""Module summary

Extended module summary

"""

from datetime import datetime
import os
import requests
import sys
import time
# Third-party modules
import ipdb
# Custom modules
import utilities.exceptions.files as files_exc
import utilities.exceptions.connection as connec_exc
from utilities.genutils import read_file, get_local_datetime, write_file
from utilities.logging.logutils import get_logger


class SaveWebpages:
    """

    Parameters
    ----------
    main_cfg
    logger
    """
    # `logger` can be a `dict` or a `LoggingWrapper` instance
    def __init__(self, main_cfg, logger):
        self.main_cfg = main_cfg
        self.logger = get_logger(__name__,
                                 __file__,
                                 os.getcwd(),
                                 logger)
        self.conn = None
        # Establish a session to be used for the GET requests
        self.req_session = requests.Session()
        self.headers = self.main_cfg['headers']
        self.last_request_time = -sys.float_info.max

    def load_cache_webpage(self, filename):
        """

        Parameters
        ----------
        filename

        Raises
        ------

        Returns
        -------

        """
        try:
            self.logger.debug(
                "Reading the cached HTML file '{}'".format(filename))
            html = read_file(filename)
        except OSError as e:
            raise OSError(e)
        else:
            self.logger.debug(
                "The webpage HTML was successfully loaded from '{}'".format(
                    filename))
            # Get the file's modified as the datetime the webpage was
            # originally accessed
            webpage_accessed = \
                datetime.fromtimestamp(os.path.getmtime(filename))
            return html, webpage_accessed

    def save_webpage(self, filename, url, overwrite_webpages=True):
        """

        Parameters
        ----------
        filename
        url
        overwrite_webpages

        Raises
        ------

        Returns
        -------

        """
        if os.path.isfile(filename) and not overwrite_webpages:
            html, webpage_accessed = self.load_cache_webpage(filename)
        else:
            # Retrieve webpage
            try:
                # Get the datetime the webpage was retrieved
                webpage_accessed = get_local_datetime()
                html = self._get_webpage(url)
            except (OSError, connec_exc.HTTP404Error) as e:
                # from `_get_webpage()`
                raise connec_exc.WebPageNotFoundError(e)
            else:
                self.logger.debug("Webpage retrieved!")
            # Write webpage locally
            try:
                self.logger.debug(
                    "Saving webpage to '{}'".format(filename))
                write_file(filename, html, overwrite_webpages)
            except (OSError, files_exc.OverwriteFileError) as e:
                raise files_exc.WebPageSavingError(e)
            else:
                self.logger.debug("The webpage is saved in '{}'. URL is "
                                  "'{}'".format(filename, url))
        return html, webpage_accessed

    def _get_webpage(self, url):
        """

        Parameters
        ----------
        url

        Raises
        ------

        Returns
        -------

        """
        current_delay = time.time() - self.last_request_time
        diff_between_delays = \
            current_delay - self.main_cfg['delay_between_requests']
        if diff_between_delays < 0:
            self.logger.debug("Waiting {} seconds before sending next HTTP "
                              "request...".format(abs(diff_between_delays)))
            time.sleep(abs(diff_between_delays))
            self.logger.debug("Time is up! HTTP request will be sent.")
        try:
            self.logger.debug("Sending HTTP request ...")
            self.last_request_time = time.time()
            # TODO: remove ipdb
            ipdb.set_trace()
            req = self.req_session.get(
                url,
                headers=self.headers,
                timeout=self.main_cfg['http_get_timeout'])
            html = req.text
        except OSError as e:
            raise OSError(e)
        else:
            if req.status_code == 404:
                raise connec_exc.WebPageNotFoundError(
                    "404 - PAGE NOT FOUND. The URL '{}' returned a 404 status "
                    "code.".format(url))
        return html
