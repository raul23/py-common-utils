"""Module summary

Extended summary

"""

import logging
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
        Name of the module, e.g. ``'utilities.databases.dbutils'``
    module_file : str
        Module's filename, e.g. run_scraper.py
    cwd : str
        Module's current working directory, e.g. .../lyrics-scraper/script
    logging_cfg : str or dict
        The logger can be setup through a logging configuration file that can
        be given either as a file path (``str``) or a dictionary (``dict``).
    use_default_colors : bool, optional
        Whether to use the default colors when working in a Unix terminal (the
        default value is False which might imply that no color will be added to
        the log messages or that the user is working in a PyCharm terminal).
    use_pycharm_colors : bool, optional
        Whether to add color to log messages when working in a PyCharm terminal
        (the default value is False which might imply that no color will be
        added to the log messages or that the user is working in a Unix
        terminal).

    """

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
            assert isinstance(logging_cfg, dict), \
                "`logging_cfg` must be a `dict`"
            try:
                logging_opts = logging_cfg['logging_options']
                self.use_default_colors = logging_opts['use_default_colors']
                self.use_pycharm_colors = logging_opts['use_pycharm_colors']
            except KeyError:
                raise KeyError(
                    "[{}] The logging configuration dict was not previously "
                    "updated with `logging_options`".format(module_name))
        # Get the console and file loggers
        c_logger, f_logger = self._get_loggers()
        # Init the logging wrapper
        self.lw = LoggingWrapper(
            c_logger,
            f_logger,
            self.use_default_colors,
            self.use_pycharm_colors)
        if self.lw.use_colors:
            self.lw.info("The log messages will be colored")
        if self.lw.use_pycharm_colors:
            self.lw.info("The colors of the logging messages are those used "
                         "for the PyCharm terminal")
        # Add the console and file loggers to the logging config ``dict`` if
        # they are not there yet
        if isinstance(logging_cfg, dict):
            self._add_loggers([c_logger, f_logger], logging_cfg)
        # Setup loggers from YAML logging configuration file or dict
        self.logging_cfg_dict = self._setup_loggers_from_cfg(logging_cfg)
        if isinstance(logging_cfg, str) and False:
            # Update the dict `config` with logging options necessary for
            # setting up the logging mechanism in the other custom modules
            # NOTE: `logging_cfg_filepath` is not used in this module
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
        """Add loggers to a logging config dictionary.

        TODO: only if the loggers are not already there

        Parameters
        ----------
        new_loggers : list of logging.Logger
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

    def _get_loggers(self):
        """Get console and file loggers.

        Init the console and file loggers

        Returns
        -------

        """
        logger_name = get_logger_name(
            self.module_name, self.module_file, self.cwd)
        c_logger = logging.getLogger(
            '{}.c'.format(logger_name))
        f_logger = logging.getLogger(
            '{}.f'.format(logger_name))
        # Clear the two loggers from any handlers
        self.remove_all_handlers(c_logger)
        self.remove_all_handlers(f_logger)
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

    def _setup_loggers_from_cfg(self, logging_cfg):
        """Setup console and file loggers from a YAML configuration file or
        logging ``dict``.

        File and console loggers will be setup through a YAML logging
        configuration file which defines the loggers, their handlers, and the
        formatters (how log messages get displayed).

        This logging config file is either given as a file path or a ``dict``.

        Also, a date and time is added to the beginning of the log filename but
        only in the case that the logging configuration file is given as a file
        path. Hence, each re-run of the script won't overwrite the previous log
        file.

        Parameters
        ----------
        logging_cfg : str or dict
            The YAML configuration file path or the logging ``dict`` that is
            used to setup the logging.

        Returns
        -------
        logging_cfg_dict : dict
            The logging configuration ``dict`` that is used to setup the
            loggers.

        Notes
        -----
        The reason why the datetime is only added to the log filename when
        `logging_cfg` refers to a file path is that this is the case where for
        the first time the log file is created, i.e. the main script is setting
        up its logging before any other custom modules.

        Thus afterwards, the other custom modules don't need to bother with the
        log filename anymore, i.e. no need to add the datetime to the log
        filename anymore since it has already been done by the main script's
        logging.

        """
        # Setup loggers from YAML logging configuration file or logging ``dict``
        try:
            if isinstance(logging_cfg, str):
                # Case: main script is setting up its logging
                # Add datetime at the beginning of the log filename
                # e.g. 2018-09-21-23-24-15-debug.log
                add_datetime = True
                self.lw.info(
                    "Setting up logging from the YAML configuration file "
                    "'{}'".format(logging_cfg))
            else:
                ipdb.set_trace()
                # Case: custom modules (other than the main script) are setting
                # up their logging
                add_datetime = False
                self.lw.info(
                    "Setting up logging from a dictionary")
            logging_cfg_dict = setup_logging_from_cfg(logging_cfg,
                                                      add_datetime=add_datetime)
        except (KeyError, OSError, ValueError) as e:
            # TODO: write the traceback with one line, see
            # https://bit.ly/2DkH63E
            self.lw.critical(e)
            # TODO: sys.exit(1)?
            # TODO: raise a custom Exception that could be caught within the
            # script
            raise SystemExit("Logging could not be setup. Program will exit.")
        else:
            self.lw.debug("Logging setup completed")
            return logging_cfg_dict

    def _update_logging_cfg_dict(self, options):
        """Update the logging config dictionary with new options.

        It updates the logging config dictionary with logging options necessary
        for setting up the logging mechanism in other custom modules.

        Parameters
        ----------
        options :

        Raises
        ------
        SystemExit
            Raised if the new logging options' keys are not unique.


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
        """Get the logger.

        Returns
        -------
        lw: logging_wrapper.LoggingWrapper


        """
        return self.lw

    @staticmethod
    def remove_all_handlers(logger):
        """Remove all handlers from a logger.

        Parameters
        ----------
        logger : logging.Logger
            The logger whose handlers will be removed.

        """
        for h in logger.handlers:
            logger.removeHandler(h)
