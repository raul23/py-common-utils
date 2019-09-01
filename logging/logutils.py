"""Module that defines logging-related functions.

"""
from datetime import datetime
import logging.config
import os
# Custom modules
from .logging_wrapper import LoggingWrapper
from utilities.genutils import read_yaml


def get_logger(module_name, module_file, cwd, logger=None):
    """Get a console or console+file logger.

    This function can build a logger from scratch, i.e. without any logging
    config ``dict``. In that case, a console logger is returned.

    Also, it can setup a console and file logger if a logging config ``dict``
    is passed.

    Parameters
    ----------
    module_name : str
        Name of the module, e.g. ``'__main__'``
    module_file : str
        Module's filename, e.g. run_scraper.py
    cwd : str
        Module's current working directory, e.g. .../lyrics-scraper/script
    logger : dict or LoggingWrapper, optional
        The logger can be setup through a logging configuration ``dict``. If a
        logger of type ``LoggingWrapper`` is passed, it implies that a logger
        is already setup and thus the same logger is returned. (the default
        value is ``None`` which implies that a console logger will be setup
        from scratch, i.e. without a logging configuration ``dict``).

    Returns
    -------
    logger : LoggingWrapper
        A logger that can log to console and file at the same time.

    Raises
    ------
    TypeError
        Raised if `logger` is not of type ``LoggingWrapper``.

    Notes
    -----
    The reason that we process the case when `logger` is already a logger of
    type ``LoggingWrapper`` is that the main script's logger can be shared
    throughout all modules, and therefore every call to this function will
    return the same logger.

    ``LoggingWrapper`` defines a logger that can log to console and file at the
    same time.

    """
    if logger is None:
        logger_name = get_logger_name(module_name, module_file, cwd)
        logger = setup_console_logger(logger_name=logger_name)
        return logger
    elif isinstance(logger, dict):
        from utilities.logging.logging_boilerplate import LoggingBoilerplate
        lb = LoggingBoilerplate(module_name,
                                module_file,
                                cwd,
                                logger)
        return lb.get_logger()
    else:
        # Sanity check on `logger`
        if isinstance(logger, LoggingWrapper):
            return logger
        else:
            # TODO: test error
            raise TypeError("`logger` must be of type ``LoggingWrapper``")


def get_logger_name(module_name, module_file, cwd):
    """Get the logger's name for a module.

    The logger's name is built based on:
    1.  the module's current working directory and its filename or
    2.  the module's name.

    The returned logger's name can then be used to setup a logger.

    Parameters
    ----------
    module_name : str
        Name of the module, e.g. ``'__main__'``
    module_file : str
        Module's filename, e.g. run_scraper.py
    cwd : str
        Module's current working directory, e.g. .../lyrics-scraper/script

    Returns
    -------
    logger_name : str
        Logger's name, e.g. script.run_scraper

    Notes
    -----
    If the module is read from script, then `module_name` will be equal to
    ``'__main__'`` [1]. In that case, the module's working directory and its
    filename will be used to build the logger's name.

    References
    ----------
    .. [1] `__main__ — Top-level script environment <https://docs.python.org/3/library/__main__.html/>`

    """
    if module_name == '__main__':
        # When the Python file (where the calling to this function is made) is
        # run as a script
        # `cwd` is the directory path of the script, e.g.
        # ~/PycharmProjects/lyrics-scraper/script
        # Get only the directory name which will be the `package_name`
        # e.g. ~/PycharmProjects/lyrics-scraper/script --> script
        package_name = os.path.basename(cwd)
        # Remove extension from filename, e.g. run_scraper.py --> run_scraper
        module_name = os.path.splitext(module_file)[0]
        logger_name = "{}.{}".format(package_name, module_name)
    else:
        # When the Python file (where the calling to this function is made) is
        # imported as a module
        if '.' in module_name:
            logger_name = module_name
        else:
            # TODO: test this case where the module name doesn't have any dot.
            package_name = os.path.basename(cwd)
            module_name = module_name
            logger_name = "{}.{}".format(package_name, module_name)
    return logger_name


def setup_console_logger(
        logger=None,
        logger_name="console_logger",
        logger_level=logging.DEBUG,
        handler_level=logging.DEBUG,
        handler_format='%(name)-30s: %(levelname)-8s %(message)s'):
    """Setup a basic console logger without a logging configuration file or
    dictionary.

    A basic **console** logger is setup with debug logging level and whose
    output format consists of its name, log level, and message.

    Parameters
    ----------
    logger : logging.Logger, optional
        A console logger (the default value is ``None`` which implies that a
        console logger will be setup from scratch, i.e. without a logging
        config ``dict``).
    logger_name : str, optional
        Logger's unique name (the default value is `console_logger`).
    logger_level : int, optional
        Logger's log level that filters out logs whose levels are inferior (the
        default value is ``DEBUG`` which implies that no logs will be ignored
        by the logger).
    handler_level : int, optional
        Handler's log level that filters out logs whose levels are inferior,
        e.g. a log handler with the INFO level will not handle DEBUG logs [1] (
        the default value is DEBUG which implie that no logs will be ignored by
        the logger's handler).
    handler_format : str, optional
        Adds context information to a log (the default value is
        ``'%(name)-30s: %(levelname)-8s %(message)s'`` which implies that each
        log record will consist of the logger's name, its log level, and the
        log's message).

    Returns
    -------
    logger : logging.Logger
        A logger that logs to the console with debug logging level .

    See Also
    --------
    setup_logging_from_cfg : uses a YAML configuration file or ``dict`` to
                             setup a logger.

    Notes
    -----
    A logging.StreamHandler() (i.e. console handler) is added to the logger's
    handlers.

    References
    ----------
    .. [1] `Python Logging: An In-Depth Tutorial <https://www.toptal.com/python/in-depth-python-logging/>`

    """
    if logger is None:
        logger = logging.getLogger(logger_name)
        # To remove duplicated logging messages: set `propagate` to False
        # ref.: https://stackoverflow.com/a/44426266
        logger.propagate = False
    handler = logging.StreamHandler()
    handler.setLevel(handler_level)
    formatter = logging.Formatter(handler_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logger_level)
    return logger


def setup_logging_from_cfg(logging_config, add_datetime=False):
    """Setup logging from a YAML configuration file or logging ``dict``.

    Loggers can be setup through a YAML logging configuration file which
    define the loggers, their handlers, and the formatters (how log messages
    get displayed).

    Also, a date and time can be added to the beginning of the log' filename.
    Hence, each re-run of the script doesn't overwrite the previous log file.

    Parameters
    ----------
    logging_config : str or dict
        The YAML configuration file path or the logging ``dict`` that is used
        to setup the logging.
    add_datetime : bool, optional
        Whether a date and time should be added at the beginning of the debug
        log filename, e.g. 2019-08-29-00-58-22-debug.log (the default value is
        ``False`` which implies that a date and time will be added at the
        start of the debug log filename).

    Returns
    -------
    config_dict : dict
        The logging configuration ``dict`` that is used to setup the logger(s).

    Raises
    ------
    KeyError
        Raised if a key in the logging config ``dict`` is not found.
    OSError
        Raised if the YAML logging config file doesn't exist.
    ValueError
        Raised if the YAML logging config is invalid, i.e. a key or value is
        invalid. Example: a handler's class is written incorrectly.

    See Also
    --------
    setup_console_logger : setup a basic console logger without a config file
                           or logging ``dict``.

    Notes
    -----
    For an example of a YAML logging configuration file, check
    `Configuring Logging <https://docs.python.org/3/howto/logging.html#configuring-logging>`_.

    """
    try:
        if isinstance(logging_config, str):
            # Read YAML configuration file
            config_dict = read_yaml(logging_config)
        else:
            config_dict = logging_config
        if add_datetime:
            # Add the datetime to the beginning of the log filename
            # ref.: https://stackoverflow.com/a/45447081
            filename = config_dict['handlers']['file']['filename']
            new_filename = '{:%Y-%m-%d-%H-%M-%S}-{}'.format(
                datetime.now(), filename)
            config_dict['handlers']['file']['filename'] = new_filename
        # Update the logging config dict with new values from `config_dict`
        logging.config.dictConfig(config_dict)
    except OSError as e:
        raise OSError(e)
    except KeyError as e:
        raise KeyError(e)
    except ValueError as e:
        raise ValueError(e)
    else:
        return config_dict
