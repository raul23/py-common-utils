"""Module that defines common logging functions.

See Also
--------
dbutils : module that defines common database functions.
genutils : module that defines many general and useful functions.


.. _Configuration dictionary schema: https://bit.ly/2lUSyLq
.. _Configuring Logging: https://bit.ly/2kyx5rj
.. _logging configuration file: https://bit.ly/2niTDgY

"""

import copy
import logging.config
import os
from datetime import datetime

from pyutils.genutils import load_yaml


def get_error_msg(exc):
    """Get an error message from an exception.

    It converts an error message of type :exc:`Exception` (e.g.
    :exc:`sqlite3.IntegrityError`) into a string to then be logged.

    TODO: give an example of how the string would look like

    Parameters
    ----------
    exc : Exception
        The error message as an :exc:`Exception`, e.g. :exc:`TypeError`, which
        will be converted to a string.

    Returns
    -------
    error_msg : str
        The error message converted as a string.

    """
    # TODO: explain
    error_msg = '[{}] {}'.format(exc.__class__.__name__, exc.__str__())
    return error_msg


def setup_basic_logger(name, add_console_handler=False, add_file_handler=False,
                       console_format=None, file_format=None,
                       log_filepath="debug.log", remove_all_handlers=False,
                       handlers_to_remove=None):
    """TODO

    Parameters
    ----------
    name
    add_console_handler
    add_file_handler
    console_format
    file_format
    log_filepath
    remove_all_handlers
    handlers_to_remove

    Returns
    -------

    """
    # TODO: explain
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if remove_all_handlers or handlers_to_remove:
        handlers = copy.copy(logger.handlers)
        for h in handlers:
            if remove_all_handlers or h in handlers_to_remove:
                logger.removeHandler(h)
    if add_console_handler:
        # Setup console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        if console_format:
            formatter = logging.Formatter(console_format)
            ch.setFormatter(formatter)
        logger.addHandler(ch)
    if add_file_handler:
        # Setup file handler
        fh = logging.FileHandler(log_filepath)
        fh.setLevel(logging.DEBUG)
        if file_format:
            formatter = logging.Formatter(console_format)
            fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


def setup_logging_from_cfg(logging_config):
    """Setup logging from a YAML configuration file or logging dictionary.

    Loggers can be setup through a YAML logging configuration file or logging
    dictionary which defines the loggers, their handlers, and the formatters
    (how log messages get displayed).

    Also, a date and time can be added to the beginning of the log filename
    by setting the option ``add_datetime`` to True in the `logging configuration
    file`_. Thus, you can generate log filenames like this::

        2019-08-29-00-58-22-debug.log

    Parameters
    ----------
    logging_config : str or dict
        The YAML configuration file path or the logging :obj:`dict` that is used
        to setup the logging.
        The contents of the logging dictionary is described in `Configuration
        dictionary schema`_.

    Returns
    -------
    config_dict : dict
        The logging configuration :obj:`dict` that is used to setup the
        logger(s). The contents of the logging dictionary is described in
        `Configuration dictionary schema`_.

    Raises
    ------
    KeyError
        Raised if a key in the logging config :obj:`dict` is not found.
    OSError
        Raised if the YAML logging config file doesn't exist.
    ValueError
        Raised if the logging config :obj:`dict` is invalid, i.e. a key or
        value is invalid. Example: a logging handler's class is written
        incorrectly.

    Notes
    -----
    For an example of a YAML logging configuration file, check `Configuring
    Logging`_.

    """
    try:
        # Check type of logging_config
        if isinstance(logging_config, str):
            # It is a YAML configuration file
            config_dict = load_yaml(logging_config)
        else:
            # It is a logging config dictionary
            config_dict = logging_config
        if config_dict.get('add_datetime'):
            # Add the datetime to the beginning of the log filename
            # ref.: https://stackoverflow.com/a/45447081
            filename = config_dict['handlers']['file']['filename']
            # In case that the filename is a path, e.g. /test/debug.log
            dirname = os.path.dirname(filename)
            filename = os.path.basename(filename)
            new_filename = '{:%Y-%m-%d-%H-%M-%S}-{}'.format(
                datetime.now(), filename)
            new_filename = os.path.join(dirname, new_filename)
            config_dict['handlers']['file']['filename'] = new_filename
        # Update the logging config dict with new values from config_dict
        logging.config.dictConfig(config_dict)
    except (KeyError, OSError, ValueError):
        raise
    else:  # No error
        return config_dict
