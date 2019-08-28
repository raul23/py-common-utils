from datetime import datetime
import logging.config
# Custom modules
from .logging_wrapper import LoggingWrapper
from utilities.genutils import read_yaml


def get_logger(module_name, module_file, cwd, logger):
    """

    Parameters
    ----------
    module_name
    module_file
    cwd
    logger

    Raises
    ------

    Returns
    -------

    """
    if isinstance(logger, dict):
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


def setup_logging(logging_config, add_datetime=False):
    """Setup logging from YAML configuration file or logging `dict`

    Parameters
    ----------
    logging_config : str or dict
        The YAML configuration file or the logging dict
    add_datetime : bool
        Description

    Raises
    ------

    Returns
    -------

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
