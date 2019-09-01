"""Module summary

Extended summary

"""

import logging
import os
# Third-party modules
import ipdb
# Custom modules
from .logutils import get_logger_name, setup_console_logger, \
    setup_logging_from_cfg
from .logging_wrapper import LoggingWrapper


class LoggingBoilerplate:
    """

    Parameters
    ----------
    module_name : str
        Description
    module_file : str
        Description
    cwd : str
        Description
    logging_cfg : str or dict
        Description
    use_default_colors : bool
        Description
    use_pycharm_colors : bool
        Description

    """

    # `logging_cfg` can either be the path to the logging configuration file
    # (i.e. a string) or the logging `dict`
    def __init__(self, module_name, module_file, cwd, logging_cfg,
                 use_default_colors=False, use_pycharm_colors=False):
        self.module_name = module_name
        self.module_file = module_file
        self.cwd = cwd
        if isinstance(logging_cfg, str):
            self.use_default_colors = use_default_colors
            self.use_pycharm_colors = use_pycharm_colors
        else:
            # Sanity check on `logging_cfg`
            assert isinstance(logging_cfg, dict), "`logging_cfg` must be a `dict`"
            logging_opts = logging_cfg['logging_options']
            self.use_default_colors = logging_opts['use_default_colors']
            self.use_pycharm_colors = logging_opts['use_pycharm_colors']
        # Get the console and file loggers
        c_logger, f_logger = self._get_loggers()
        # Init the logging wrapper
        self.lw = LoggingWrapper(
            c_logger, f_logger, self.use_default_colors, self.use_pycharm_colors)
        if self.lw.use_colors:
            self.lw.info("The log messages will be colored")
        if self.lw.use_pycharm_colors:
            self.lw.info("The colors of the logging messages are those used "
                         "for the Pycharm Terminal")
        # Add the console and file loggers to the logging config file if they
        # are not there yet
        if isinstance(logging_cfg, dict):
            self._add_loggers([c_logger, f_logger], logging_cfg)
        # Setup loggers from YAML logging configuration file or dict
        self.logging_cfg_dict = self._setup_loggers_from_cfg(logging_cfg)
        if isinstance(logging_cfg, str):
            # Update the dict `config` with logging options necessary for setting
            # up the logging mechanism in the other modules,
            # e.g. `industries_analyzer.py`
            # NOTE: `logging_cfg_filepath` not used in this module
            logging_options = {
                'logging_options':
                    {
                        'logging_cfg_filepath': logging_cfg,
                        'use_default_colors': use_default_colors,
                        'use_pycharm_colors': use_pycharm_colors
                    }
            }
            self._update_logging_cfg_dict(logging_options)

    # Add loggers to logging config dict
    @staticmethod
    def _add_loggers(new_loggers, logging_cfg):
        """

        Parameters
        ----------
        new_loggers : list of logger
            Description
        logging_cfg : dict
            Description

        """
        for new_logger in new_loggers:
            for old_logger_name in logging_cfg['loggers'].keys():
                if new_logger.name[-2:] == old_logger_name[-2:]:
                    value = logging_cfg['loggers'][old_logger_name]
                    # del logging_cfg['loggers'][old_logger_name]
                    logging_cfg['loggers'][new_logger.name] = value
                    break

    # Init the console and file loggers
    def _get_loggers(self):
        """

        Returns
        -------

        """
        logger_name = get_logger_name(
            self.module_name, self.module_file, self.cwd)
        # TODO: I could create one logger that can log into the console and a
        # file. But since the console's log messages can be colored, the file's
        # log messages will have color information. I could remove the file
        # handler every time I log into the console, and then add it again when
        # it is time to log into the file. Or there is a better solution.
        c_logger = logging.getLogger(
            '{}.c'.format(logger_name))
        f_logger = logging.getLogger(
            '{}.f'.format(logger_name))
        # Clear the two loggers from any handlers
        self.remove_handlers(c_logger)
        self.remove_handlers(f_logger)
        # Setup console logger WITHOUT configuration file
        # IMPORTANT: the file logger will not be setup completely yet, i.e. no
        # handler added. The file logger will be setup later on from the YAML
        # configuration file
        # To remove duplicated logging messages: set `propagate` to False
        # ref.: https://stackoverflow.com/a/44426266
        c_logger.propagate = False
        f_logger.propagate = False
        setup_console_logger(logger=c_logger)
        return c_logger, f_logger

    # `logging_cfg` is the absolute path of the logging configuration file
    # or a logging ``dict``
    def _setup_loggers_from_cfg(self, logging_cfg):
        """

        Parameters
        ----------
        logging_cfg

        Returns
        -------

        """
        # TODO: not needed anymore
        # logging_cfg = os.path.realpath(logging_cfg)
        # Setup loggers from YAML logging configuration file or logging `dict`
        try:
            if isinstance(logging_cfg, str):
                # Add datetime at the beginning of the log filename
                # e.g. 2018-09-21-23-24-15-debug.log
                add_datetime = True
                self.lw.info(
                    "Setting up logging from the YAML configuration file "
                    "'{}'".format(logging_cfg))
            else:
                add_datetime = False
                self.lw.info(
                    "Setting up logging from a dictionary")
            logging_cfg_dict = setup_logging_from_cfg(logging_cfg, add_datetime=add_datetime)
        except (KeyError, OSError, ValueError) as e:
            # TODO: write the traceback with one line, see https://bit.ly/2DkH63E
            self.lw.critical(e)
            # TODO: sys.exit(1)?
            # TODO: raise a custom Exception that could be caught within the script
            raise SystemExit("Logging could not be setup. Program will exit.")
        else:
            self.lw.debug("Logging setup completed")
            return logging_cfg_dict

    def _update_logging_cfg_dict(self, options):
        """

        Parameters
        ----------
        options

        """
        self.lw.debug(
            "Updating the logging config dict with logging options: "
            "{}".format(options))
        cfg_keys_set = set(self.logging_cfg_dict.keys())
        options_keys_set = set(options.keys())
        result_set = cfg_keys_set.intersection(options_keys_set)
        if result_set:
            # TODO: raise a custom Exception
            self.lw.debug("The logging options' keys are not unique")
            raise SystemExit("Program will exit.")
        else:
            self.logging_cfg_dict.update(options)

    def get_logger(self):
        """

        Returns
        -------

        """
        return self.lw

    @staticmethod
    def remove_handlers(logger):
        """

        Parameters
        ----------
        logger

        """
        for h in logger.handlers:
            logger.removeHandler(h)
