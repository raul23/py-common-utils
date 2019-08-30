from datetime import datetime
import logging.config
import os
# Custom modules
from .logging_wrapper import LoggingWrapper
from utilities.genutils import read_yaml


def get_logger(module_name, module_file, cwd, logger=None):
    """

    Parameters
    ----------
    module_name
    module_file
    cwd
    logger : dict or LoggingWrapper, optional

    Returns
    -------

    Raises
    ------
    TypeError
        Raised if

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
            raise TypeError("`logger` must be of type `LoggingWrapper`")


def get_logger_name(module_name, module_file, cwd):
    if module_name == '__main__':
        # When the Python file (where the calling to this function is made) is
        # run as a script
        package_name = os.path.basename(cwd)
        module_name = os.path.splitext(module_file)[0]
    else:
        # When the Python file (where the calling to this function is made) is
        # imported as a module
        if '.' in module_name:
            # NOTE: this work even when there are two dots in the module name,
            # e.g. utilities.databases.dbutils
            # In this example, the package name is 'utilities.databases' and
            # the module name is 'db_utils'
            temp = module_name
            # Find index of last dot
            index = module_name.rfind('.')
            module_name = module_name[index+1:]
            temp = temp[:index]
            # Find index of second to last dot
            index = temp.rfind('.')
            package_name = temp[index+1:]
        else:
            # TODO: test
            package_name = os.path.basename(cwd)
            module_name = module_name
    return "{}.{}".format(package_name, module_name)


def setup_console_logger(
        logger=None,
        logger_name="",
        logger_level=logging.DEBUG,
        handler_level=logging.DEBUG,
        handler=logging.StreamHandler(),
        handler_format='%(name)-30s: %(levelname)-8s %(message)s'):
    """Setup logger without a logging configuration file or dictionary.

    A basic **console** logger is setup with debug logging level and whose
    output format consists of its name, log level, and message.

    If you need to setup a more complex logger, see  setup_logging_from_cfg()
    which makes use of a YAML configuration file or ``dict`` to setup the
    logger.

    Parameters
    ----------
    logger
    logger_name
    logger_level
    handler_level
    handler
    handler_format

    Returns
    -------
    logger :

    """
    if logger is None:
        logger = logging.getLogger(logger_name)
        # To remove duplicated logging messages: set `propagate` to False
        # ref.: https://stackoverflow.com/a/44426266
        logger.propagate = False
    handler.setLevel(handler_level)
    formatter = logging.Formatter(handler_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logger_level)
    return logger


def setup_logging_from_cfg(logging_config, add_datetime=False):
    """Setup logging from YAML configuration file or logging ``dict``.

    Parameters
    ----------
    logging_config : str or dict
        The YAML configuration file or the logging ``dict`` that is used to
        setup the logging.
    add_datetime : bool
        Whether a date and time should be added at the beginning of the
        debug log filename, e.g. 2019-08-29-00-58-22-debug.log

    Returns
    -------
    config_dict : dict
        Description

    Raises
    ------
    KeyError
        Raise if
    OSError
        Raise if
    ValueError
        Raise if

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
