"""Module that defines logging-related functions.

See Also
--------
utils.databases.dbutils : module that defines database-related functions.
utils.genutils : defines many general and useful functions.

"""
from datetime import datetime
import logging.config
# Custom modules
from utils.genutils import read_yaml


def get_error_msg(exc):
    """Get an error message from an exception.

    It converts an error message of type ``Exception`` (e.g.
    ``sqlite3.IntegrityError``) into a string to then be logged.

    Parameters
    ----------
    exc : Exception
        The error message as an ``Exception``, e.g. ``TypeError``, which
        will be converted to a string.

    Returns
    -------
    error_msg : str
        The error message converted as a string.

    """
    error_msg = '[{}] {}'.format(exc.__class__.__name__, exc.__str__())
    return error_msg


def setup_logging_from_cfg(logging_config):
    """Setup logging from a YAML configuration file or logging dictionary.

    Loggers can be setup through a YAML logging configuration file or logging
    dictionary which defines the loggers, their handlers, and the formatters
    (how log messages get displayed).

    Also, a date and time can be added to the beginning of the log filename
    by setting the option `add_datetime` to True in the logging configuration
    file/dict [1]. Thus, you can generate log filenames like:
                         2019-08-29-00-58-22-debug.log

    Parameters
    ----------
    logging_config : str or dict
        The YAML configuration file path or the logging ``dict`` that is used
        to setup the logging.
        The contents of the logging dictionary is described in `Configuration
        dictionary schema <https://bit.ly/2lUSyLq>`_.

    Returns
    -------
    config_dict : dict
        The logging configuration ``dict`` that is used to setup the logger(s).
        The contents of the logging dictionary is described in `Configuration
        dictionary schema <https://bit.ly/2lUSyLq>`_.

    Raises
    ------
    KeyError
        Raised if a key in the logging config ``dict`` is not found.
    OSError
        Raised if the YAML logging config file doesn't exist.
    ValueError
        Raised if the YAML logging config is invalid, i.e. a key or value is
        invalid. Example: a logging handler's class is written incorrectly.

    Notes
    -----
    For an example of a YAML logging configuration file, check `Configuring
    Logging <https://bit.ly/2kyx5rj>`_.

    References
    ----------
    .. [1] `GitHub: logging_cfg.yaml <https://bit.ly/2lNMx32/>`_.

    """
    try:
        # Check type of logging_config
        if isinstance(logging_config, str):
            # It is a YAML configuration file
            config_dict = read_yaml(logging_config)
        else:
            # It is a logging config dictionary
            config_dict = logging_config
        if config_dict.get('add_datetime'):
            # Add the datetime to the beginning of the log filename
            # ref.: https://stackoverflow.com/a/45447081
            filename = config_dict['handlers']['file']['filename']
            new_filename = '{:%Y-%m-%d-%H-%M-%S}-{}'.format(
                datetime.now(), filename)
            config_dict['handlers']['file']['filename'] = new_filename
        # Update the logging config dict with new values from config_dict
        logging.config.dictConfig(config_dict)
    except OSError as e:
        raise OSError(e)
    except KeyError as e:
        raise KeyError(e)
    except ValueError as e:
        raise ValueError(e)
    else:
        return config_dict
