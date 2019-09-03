"""Module that defines that allows you to log messages with color.

The module defines a class ``LoggingWrapper`` that creates an API for logging
messages with colors where each color represents a log level (by default the
debug messages are displayed in green).

The log messages can also be colored depending on the type of terminal:
* standard Unix terminal
* PyCharm terminal

Attributes
----------
log_levels : list of str
    The list of logging levels' names as supported by Python's ``logging``.
color_levels_template : dict
    Dictionary that defines a template for writing messages with colors based
    on the name of the log level
default_color_levels : dict
    Colors for the different log level when working on the standard Unix
    terminal.
pycharm_color_levels : dict
    Colors for the different log level when working on the PyCharm terminal.

Notes
-----
The reason for treating separately the two different types of terminal is that
the PyCharm terminal might display color levels differently than the standard
Unix terminal.

For example, the color code '32' will display as yellow on a PyCharm terminal
and green on a Unix terminal (macOS). You can test it with
`print("\033[32mtest\033[0m")`.

It's only the log messages that can be colored, not the whole log record (like
the module name or the level name).

"""

import logging


log_levels = ['debug', 'info', 'warning', 'error', 'exception', 'critical']

color_levels_template = {
    'debug':        "\033[{}m{}\033[0m",
    'info':         "\033[{}m{}\033[0m",
    'warning':      "\033[{}m{}\033[0m",
    'error':        "\033[{}m{}\033[0m",
    'exception':    "\033[{}m{}\033[0m",
    'critical':     "\033[7;31;{}m{}\033[0m"
}

# Level colors for the standard Unix Terminal
default_color_levels = {
        'debug':     36,    # Blue
        'info':      32,    # Green
        'warning':   33,    # Yellow
        'error':     31,    # Red
        'exception': 31,    # Red
        'critical':  31     # Red highlighted
}

# Level colors for the PyCharm Terminal
pycharm_color_levels = {
    'debug':     34,    # Blue
    'info':      36,    # Blue aqua
    'warning':   32,    # Yellow
    'error':     31,    # Red
    'exception': 31,    # Red
    'critical':  31     # Red highlighted
}


class LoggingWrapper:
    """A class that allows you to add color to log messages

    This class is a wrapper around ``logging.Logger`` that allows you to add
    color to your log messages.

    By calling only one of the pubic logging method (e.g. warning and critical),
    the message can be logged with color, where each color is associated to a
    log level (e.g. by default the debug messages are displayed in green).

    Parameters
    ----------
    logger : logging.Logger
        A logger for logging to console and/or file.
    use_default_colors : bool, optional
        Whether to use the default colors when working in a Unix terminal (the
        default value is False which might imply that no color will be added to
        the log messages or that the user is working in a PyCharm terminal).
    use_pycharm_colors : bool, optional
        Whether to add color to log messages when working in a PyCharm terminal
        (the default value is False which might imply that no color will be
        added to the log messages or that the user is working in a Unix
        terminal).
    color_levels : dict, optional
        The dictionary that defines the colors for the different log level (the
        default value is `default_color_levels` which implies that the colors
        as defined for the Unix terminal will be used).

    """

    def __init__(self, logger, use_default_colors=False,
                 use_pycharm_colors=False, color_levels=default_color_levels):
        # TODO: add option to change `color_levels` from the logging config file.
        # Right now, we only have two sets of color levels to choose from:
        # `default_color_levels` and `pycharm_color_levels`
        self.logger = logger
        self.use_default_colors = use_default_colors
        self.use_pycharm_colors = use_pycharm_colors
        self.color_levels = color_levels
        if self.use_pycharm_colors:
            self.color_levels = pycharm_color_levels
        if self.use_default_colors or self.use_pycharm_colors:
            self.use_colors = True
        else:
            self.use_colors = False

    def _call_loggers(self, msg, level):
        """Call the logger by adding color to the messages.

        This method calls the loggers' logging methods to write a message with
        color (if specified).

        Obviously, only the console logger gets its message colored, not the
        file logger.

        Parameters
        ----------
        msg : str or Exception
            The message (``str``) to be logged. The message can also be an
            ``Exception`` object, e.g. ``TypeError`` or
            ``sqlite3.IntegrityError``, which will be converted to a string
            (see _get_error_msg). Obviously, the message should be an
            ``Exception`` if the log level is 'error', 'exception' or
            'critical'.
        level : str
            The name of the log level, e.g. 'debug', 'info'.

        """
        # import ipdb
        # If `msg` is an ``Exception``, process the ``Exception`` to build the
        # error message as a string
        msg = self._get_error_msg(msg) if isinstance(msg, Exception) else msg
        # Get the corresponding message-logging functions (e.g. logger.info or
        # logger.debug) for the logger
        logger_method = self.logger.__getattribute__(level)
        # Only the console logger gets colored messages. The file logger don't.
        # Get the log message with colored code for the console logger
        c_msg = self._set_color(msg, level) if self.use_colors else msg
        # Disable the other non-console loggers
        removed_handlers = []
        if len(self.logger.handlers) > 1:
            for h in self.logger.handlers:
                if type(h) is not logging.StreamHandler:
                    removed_handlers.append(h)
                    self.logger.removeHandler(h)
            # Call the message-logging functions, e.g. logger.info()
            if self.logger.handlers:
                logger_method(c_msg)
            for h in removed_handlers:
                self.logger.addHandler(h)
            removed_handlers = []
            for h in self.logger.handlers:
                if type(h) is logging.StreamHandler:
                    removed_handlers.append(h)
                    self.logger.removeHandler(h)
            if self.logger.handlers:
                logger_method(msg)
            for h in removed_handlers:
                self.logger.addHandler(h)
        else:
            # Call the message-logging functions, e.g. logger.info()
            logger_method(c_msg)

    @staticmethod
    def _get_error_msg(exc):
        """Get an error message from an exception.

        It converts an error message of type ``Exception`` (e.g.
        ``sqlite3.IntegrityError`` into a string to be then logged.

        Parameters
        ----------
        exc : Exception
            The error message as an ``Exception``, e.g. ``TypeError``, which
            will converted to a string.

        Returns
        -------
        error_msg : str
            The error message converted as a string.

        """
        error_msg = '[{}] {}'.format(exc.__class__.__name__, exc.__str__())
        return error_msg

    def _set_color(self, msg, level):
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

        References
        ----------
        TODO: add link for coloring log messages,https://stackoverflow.com/a/45924203


        """
        color = self.color_levels[level]
        return color_levels_template[level].format(color, msg)

    # Logging methods
    def debug(self, msg):
        """Log a message with the 'debug' log level.

        Parameters
        ----------
        msg : str
            The message to be logged.

        """
        self._call_loggers(msg, 'debug')

    def info(self, msg):
        """Log a message with the 'info' log level.

        TODO: message can be colored

        Parameters
        ----------
        msg : str
            The message to be logged in a console and file.

        """
        self._call_loggers(msg, 'info')

    def warning(self, msg):
        """Log a message with the 'warning' log level.

        Parameters
        ----------
        msg : str
            The message to be logged.

        """
        self._call_loggers(msg, 'warning')

    def error(self, msg):
        """Log a message with the 'error' log level.

        Parameters
        ----------
        msg : str or Exception
             The message (``str``) to be logged. The message can also be an
            ``Exception`` object, e.g. ``TypeError`` or
            ``sqlite3.IntegrityError``, which will be converted to a string
            (see _get_error_msg).

        """
        self._call_loggers(msg, 'error')

    def exception(self, msg):
        """Log a message with the 'exception' log level.

        Parameters
        ----------
        msg : str or Exception
             The message (``str``) to be logged. The message can also be an
            ``Exception`` object, e.g. ``TypeError`` or
            ``sqlite3.IntegrityError``, which will be converted to a string
            (see _get_error_msg).
        """
        self._call_loggers(msg, 'exception')

    def critical(self, msg):
        """Log a message with the 'critical' log level.

        Parameters
        ----------
        msg : str or Exception
            The message (``str``) to be logged. The message can also be an
            ``Exception`` object, e.g. ``TypeError`` or
            ``sqlite3.IntegrityError``, which will be converted to a string
            (see _get_error_msg).
        """
        self._call_loggers(msg, 'critical')
