"""Module summary

Extended summary

Attributes
----------
log_levels : list of str
    Description
color_levels_template : dict
    Description
default_color_levels : dict
    Description
pycharm_color_levels : dict
    Description

"""

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

# Level colors for the Pycharm Terminal
pycharm_color_levels = {
    'debug':     34,    # Blue
    'info':      36,    # Blue aqua
    'warning':   32,    # Yellow
    'error':     31,    # Red
    'exception': 31,    # Red
    'critical':  31     # Red highlighted
}


class LoggingWrapper:
    """

    Parameters
    ----------
    c_logger
    f_logger
    use_default_colors
    use_pycharm_colors
    color_levels

    """

    # TODO: add option to change `color_levels` from the logging config file
    # Right now, we only have two sets of color levels to choose from:
    # `default_color_levels` and `pycharm_color_levels`
    def __init__(self, c_logger, f_logger, use_default_colors=False,
                 use_pycharm_colors=False, color_levels=default_color_levels):
        self.c_logger = c_logger
        self.f_logger = f_logger
        self.use_default_colors = use_default_colors
        self.use_pycharm_colors = use_pycharm_colors
        self.color_levels = color_levels
        if self.use_pycharm_colors:
            self.color_levels = pycharm_color_levels
        if self.use_default_colors or self.use_pycharm_colors:
            self.use_colors = True
        else:
            self.use_colors = False

    # `msg` can either be a string or an Exception object (e.g. TypeError)
    def _call_loggers(self, msg, level):
        """

        Parameters
        ----------
        msg : str
        level : str

        """
        # If `msg` is an Exception, process the Exception to build the error
        # message
        msg = self._get_error_msg(msg) if isinstance(msg, Exception) else msg
        # Get the corresponding message-logging functions (e.g. logger.info or
        # logger.debug) for each of the two loggers
        c_logger_method = self.c_logger.__getattribute__(level)
        f_logger_method = self.f_logger.__getattribute__(level)
        # Only the console logger gets colored messages. The file logger don't.
        c_msg = self._set_color(msg, level) if self.use_colors else msg
        # Call the message-logging functions, e.g. logger.info()
        c_logger_method(c_msg)
        f_logger_method(msg)

    @staticmethod
    def _get_error_msg(exc):
        """

        Parameters
        ----------
        exc

        Returns
        -------

        """
        error_msg = '[{}] {}'.format(exc.__class__.__name__, exc.__str__())
        return error_msg

    # Color the logging message
    # ref.: https://stackoverflow.com/a/45924203
    def _set_color(self, msg, level):
        """

        Parameters
        ----------
        msg
        level

        """
        color = self.color_levels[level]
        return color_levels_template[level].format(color, msg)

    # Logging methods
    def debug(self, msg):
        """

        Parameters
        ----------
        msg

        """
        self._call_loggers(msg, 'debug')

    def info(self, msg):
        """

        Parameters
        ----------
        msg

        """
        self._call_loggers(msg, 'info')

    def warning(self, msg):
        """

        Parameters
        ----------
        msg

        """
        self._call_loggers(msg, 'warning')

    # Note for both `error()` and `exception()`:
    # msg can be either a string or an 'Exception` object
    def error(self, msg):
        """

        Parameters
        ----------
        msg

        """
        self._call_loggers(msg, 'error')

    def exception(self, msg):
        """

        Parameters
        ----------
        msg

        """
        self._call_loggers(msg, 'exception')

    def critical(self, msg):
        """

        Parameters
        ----------
        msg

        """
        self._call_loggers(msg, 'critical')
