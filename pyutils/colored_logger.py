"""Module that allows you to log messages with color.

The module defines a class ``LoggingWrapper`` that creates an API for logging
messages with colors where each color represents a log level (e.g. by default
the debug messages are displayed in blue).

The log messages can also be colored depending on the type of terminal:
- standard Unix terminal
- PyCharm terminal

Attributes
----------
_nameToLevel : list of str
    The list of logging levels' names as supported by :mod:`logging`.
_levelToColoredMessage : dict
    Dictionary that defines a template for writing messages with colors based
    on the name of the log level.
    Its keys are the names of the log levels (e.g. debug and info) and its
    values are strings that consist of ANSI escape sequences with placeholders
    for the color code and the log message.
_unixLevelToColor : dict
    Colors for the different log levels when working on the standard Unix
    terminal.
    Its keys are the names of the log levels (e.g. debug and info) and its
    values are the color code.
_pycharmLevelToColor : dict
    Colors for the different log levels when working on the PyCharm terminal.
    Its keys are the names of the log levels (e.g. debug and info) and its
    values are the color code.

Notes
-----
The reason for treating separately the two different types of terminal is that
the PyCharm terminal will display color codes differently than the standard
Unix terminal.

For example, the color code '32' will display as yellow on a PyCharm terminal
and green on a Unix terminal (macOS). You can test it with
`print("\033[32mtest\033[0m")`.

It's only the log messages that can be colored, not the whole log record (like
the module name or the level name).

"""

import logging
import os
from logging import getLevelName, Logger, StreamHandler, NOTSET

from pyutils.logutils import get_error_msg
import ipdb


# WARN = WARNING and FATAL = CRITICAL
_levels = ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG',
           'NOTSET']

# TODO: explain, incl. CRITICAL different code than other levels (highlight)
_levelToColoredMessage = {
    'NOTSET':       "\033[{}m{}\033[0m",
    'DEBUG':        "\033[{}m{}\033[0m",
    'INFO':         "\033[{}m{}\033[0m",
    'WARNING':      "\033[{}m{}\033[0m",
    'ERROR':        "\033[{}m{}\033[0m",
    'EXCEPTION':    "\033[{}m{}\033[0m",
    'CRITICAL':     "\033[7;31;{}m{}\033[0m"
}
_levelToColoredMessage['WARN'] = _levelToColoredMessage['WARNING']

# Color codes for the log levels in the production environment
_prodLevelToColorCode = {
    'NOTSET':    36,    # Blue
    'DEBUG':     36,    # Blue
    'INFO':      32,    # Green
    'WARNING':   33,    # Yellow
    'ERROR':     31,    # Red
    'EXCEPTION': 31,    # Red
    'CRITICAL':  31     # Red highlighted
}
_prodLevelToColorCode['WARN'] = _prodLevelToColorCode['WARNING']

# Color codes for the log levels in the development environment (Pycharm)
_devLevelToColorCode = {
    'NOTSET':    34,    # Blue
    'DEBUG':     34,    # Blue
    'INFO':      36,    # Blue aqua
    'WARNING':   32,    # Yellow
    'ERROR':     31,    # Red
    'EXCEPTION': 31,    # Red
    'CRITICAL':  31     # Red highlighted
}
_devLevelToColorCode['WARN'] = _devLevelToColorCode['WARNING']

# TODO: explain
_envToColorCodes = {
    'PROD': _prodLevelToColorCode,
    'DEV': _devLevelToColorCode
}


def list_to_str(list_):
    """Convert a list of strings into a single string.

    Parameters
    ----------
    list_ : list of str
        List of strings to be converted into a single string.

    Returns
    -------
    str_ : str
        The converted string.

    """
    return ", ".join(map(lambda a: "'{}'".format(a), list_))


class ColoredLogger(Logger):
    """A class that allows you to add color to log messages.

    This class is a wrapper around :class:`logging.Logger` that allows you to
    add color to log messages.

    By calling one of the pubic logging method (e.g. warning and critical), the
    message can be logged with color, where each color is associated to a log
    level (e.g. by default the debug messages are displayed in blue).

    Parameters
    ----------
    terminal : str, {None, 'UNIX', 'PYCHARM'}, optional
        The type of terminal used: 'u' for a Unix terminal and 'p' for a
        PyCharm terminal. Each terminal displays color codes differently (the
        default value is 'u').
    level_to_color : dict, optional
        The dictionary that defines the colors for the different log levels
        (the default value is `_unixLevelToColor` which implies that the
        colors as defined for the Unix terminal will be used).

        Its keys are the names of the log levels (e.g. debug and info) and its
        values are the color code used in ANSI escape sequences.

    Methods
    -------
    debug()
        Log a message with the DEBUG log level
    info()
        Log a message with the INFO log level
    warning()
        Log a message with the WARNING log level
    error()
        Log a message with the ERROR log level
    exception()
        Log a message with the EXCEPTION log level
    critical()
        Log a message with the CRITICAL log level

    Raises
    ------
    LoggingWrapperSanityCheckError
        Raised in `__init__()` if the sanity check on one of the
        ``LoggingWrapper`` parameters fails.

    """

    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)
        self._env = "DEV" if bool(os.environ.get("PYCHARM_HOSTED")) else "PROD"
        self._level_to_color = _envToColorCodes[self._env]
        self._removed_handlers = []

    def _log_with_color(self, logging_fnc, msg, level, *args, **kwargs):
        """Call the specified logging function by adding color to the messages.

        This method calls the logger's logging method to write a message with
        color (if specified).

        Only the console handler gets its message colored, not the other type
        of handlers, e.g. file handler.

        Parameters
        ----------
        msg : str or Exception
            The message (``str``) to be logged. The message can also be an
            ``Exception`` object, e.g. ``TypeError`` or
            ``sqlite3.IntegrityError``, which will be converted to a string
            (see get_error_msg). The message should be an ``Exception`` if the
            log level is 'error', 'exception' or 'critical'.
        level : str
            The name of the log level, e.g. 'debug' and 'info'.

        """
        # If msg is an Exception, process the Exception to build the
        # error message as a string
        msg = get_error_msg(msg) if isinstance(msg, Exception) else msg
        # IMPORTANT: Only the console handler gets colored messages. The file
        # handler don't.
        # Get the log message with color code for the console handler
        c_msg = self._add_color_to_msg(msg, level)
        # Disable the other non-console handlers when logging in the console.
        # Hence, the color code will not appear in the log file.
        # Remove non-console handlers from the logger
        self._remove_non_console_handlers()
        # NOTE: it is possible that no console handlers are to be found
        # since the user might have set the logger to log to a file only
        # for example.
        # Log the colored message in the console
        if self.handlers:
            # Call the message-logging function, e.g. logger.info()
            logging_fnc(c_msg, *args, **kwargs)
        # Re-add the removed non-console handlers back to the logger
        self._add_removed_handlers()
        # Remove the console handlers from the logger since we are now
        # going to log with non-console handlers
        self._remove_console_handlers()
        # Log the non-colored message with the non-console handlers
        if self.handlers:
            logging_fnc(msg, *args, **kwargs)
        # Re-add the removed console handlers back to the logger
        self._add_removed_handlers()

    def _add_removed_handlers(self):
        """Re-add the removed handlers back to the logger.

        """
        for h in self._removed_handlers:
            self.addHandler(h)
        self._removed_handlers = []

    def _remove_handler(self, h):
        """Remove a handler from the logger.

        Parameters
        ----------
        h : logging.Handler
            The handler to be removed from the logger.

        """
        self._removed_handlers.append(h)
        self.removeHandler(h)

    def _remove_console_handlers(self):
        """TODO

        """
        self._removed_handlers = []
        for h in self.handlers:
            # if type(h) is StreamHandler:
            if isinstance(h, StreamHandler):
                # Remove the console handler and save it to re-add it again
                # afterward
                self._remove_handler(h)

    def _remove_non_console_handlers(self):
        """TODO

        """
        self._removed_handlers = []
        for h in self.handlers:
            if not isinstance(h, StreamHandler):
                # Remove the non-console handler and save it to re-add it again
                # afterward
                self._remove_handler(h)

    def _add_color_to_msg(self, msg, level):
        """Add color to the log message.

        Add color to the log message based on the log level (e.g. by default
        the debug messages are displayed in green).

        Parameters
        ----------
        msg : str
            The message to be logged.
        level : str
            The name of the log level associated with log message, e.g. 'debug'
            or 'info'.

        Notes
        -----
        The code for adding color to log messages is based on the Stack
        Overflow user wahwahwah's answer to his own question about getting the
        current log level in python logging module [1].

        References
        ----------
        .. [1] `How to get the current log level in python logging module
        https://stackoverflow.com/a/45924203`_.

        """
        level = level.upper()
        color = self._level_to_color[level]
        return _levelToColoredMessage[level].format(color, msg)

    # Logging methods start here
    def debug(self, msg, *args, **kwargs):
        """Log a message with the 'debug' log level.

        Parameters
        ----------
        msg : str
            The message to be logged.

        """
        self._log_with_color(super().debug, msg, 'debug', *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Log a message with the INFO log level.

        TODO: message can be colored

        Parameters
        ----------
        msg : str
            The message to be logged in a console and file.

        """
        self._log_with_color(super().info, msg, 'info', *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Log a message with the WARNING log level.

        Parameters
        ----------
        msg : str
            The message to be logged.

        """
        self._log_with_color(super().warning, msg, 'warning', *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Log a message with the ERROR log level.

        Parameters
        ----------
        msg : str or Exception
             The message (``str``) to be logged. The message can also be an
            ``Exception`` object, e.g. ``TypeError`` or
            ``sqlite3.IntegrityError``, which will be converted to a string
            (see get_error_msg).

        """
        self._log_with_color(super().error, msg, 'error', *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """Log a message with the EXCEPTION log level.

        Parameters
        ----------
        msg : str or Exception
             The message (``str``) to be logged. The message can also be an
            ``Exception`` object, e.g. ``TypeError`` or
            ``sqlite3.IntegrityError``, which will be converted to a string
            (see get_error_msg).
        """
        self._log_with_color(super().exception, msg, 'exception', *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """Log a message with the EXCEPTION log level.

        Parameters
        ----------
        msg : str or Exception
            The message (``str``) to be logged. The message can also be an
            ``Exception`` object, e.g. ``TypeError`` or
            ``sqlite3.IntegrityError``, which will be converted to a string
            (see get_error_msg).
        """
        self._log_with_color(super().critical, msg, 'critical', *args, **kwargs)

    def __repr__(self):
        level = getLevelName(self.getEffectiveLevel())
        return '<%s %s (%s)>' % (self.__class__.__name__, self.name, level)
