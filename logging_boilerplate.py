import logging
import os
# Third-party modules
import ipdb
# Own modules
from .genutil import setup_logging
from .logging_wrapper import LoggingWrapper


class LoggingBoilerplate:
    # `logging_cfg` can either be the path to the logging configuration file
    # or the logging `dict`
    def __init__(self, module_name, module_file, cwd, logging_cfg,
                 use_default_colors=False, use_pycharm_colors=False):
        self.module_name = module_name
        self.module_file = module_file
        self.cwd = cwd
        if isinstance(logging_cfg, str):
            self.use_default_colors = use_default_colors
            self.use_pycharm_colors = use_pycharm_colors
        else:
            self.use_default_colors = logging_cfg['logging_options']['use_default_colors']
            self.use_pycharm_colors = logging_cfg['logging_options']['use_pycharm_colors']
        # Get the loggers
        c_logger, f_logger = self._get_loggers()
        # Init the logging wrapper
        self.lw = LoggingWrapper(
            c_logger, f_logger, self.use_default_colors, self.use_pycharm_colors)
        if self.lw.use_colors:
            self.lw.info("The log messages will be colored")
        if self.lw.use_pycharm_colors:
            self.lw.info("The colors of the logging messages are those used "
                         "for the Pycharm Terminal")
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

    # Init the console and file loggers
    def _get_loggers(self):
        if self.module_name == '__main__':
            # When it is run as a script
            package_name = os.path.basename(self.cwd)
            module_name = os.path.splitext(self.module_file)[0]
        else:
            # When it is imported as a module
            if '.' in self.module_name:
                package_name, module_name = self.module_name.split('.')
            else:
                package_name = os.path.basename(self.cwd)
                module_name = self.module_name
        # TODO: I could create one logger that logs into the console and a
        # file. But since the console's log messages can be colored, the file's
        # log messages will have color information. I could remove the file
        # handler every time I log into the console, and then add it again when
        # it is time to log into the file. Or there is a better solution.
        c_logger = logging.getLogger(
            '{}.{}.c'.format(package_name, module_name))
        f_logger = logging.getLogger(
            '{}.{}.f'.format(package_name, module_name))
        # Clear the two loggers from any handlers
        self.remove_handlers(c_logger)
        self.remove_handlers(f_logger)
        # Setup console logger WITHOUT configuration file
        # IMPORTANT: the file logger will not be setup yet, i.e. no handler
        # added. The file logger will be setup later on from the YAML
        # configuration file
        # To remove duplicated logging messages: propagate set to False
        # ref.: https://stackoverflow.com/a/44426266
        c_logger.propagate = False
        f_logger.propagate = False
        self.setup_logger(c_logger)
        return c_logger, f_logger

    # `logging_cfg` is the absolute path of the logging configuration file
    # or a logging `dict`
    def _setup_loggers_from_cfg(self, logging_cfg):
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
            logging_cfg_dict = setup_logging(logging_cfg, add_datetime=add_datetime)
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
        self.lw.debug(
            "Updating the logging config dict with logging options: "
            "{}".format(options))
        cfg_keys_set = set(self.logging_cfg_dict.keys())
        options_keys_set = set(options.keys())
        result_set = cfg_keys_set.intersection(options_keys_set)
        if result_set:
            # TODO: raise a custom Exception that could be caught in
            # run_data_analysis.py
            self.lw.debug("The logging options' keys are not unique")
            raise SystemExit("Program will exit.")
        else:
            self.logging_cfg_dict.update(options)

    def get_logger(self):
        return self.lw

    @staticmethod
    def remove_handlers(logger):
        for h in logger.handlers:
            logger.removeHandler(h)

    @staticmethod
    # Setup logger without the logging configuration
    def setup_logger(logger, logger_level=logging.DEBUG,
                     handler_level=logging.DEBUG, handler=logging.StreamHandler(),
                     handler_format='%(name)-30s: %(levelname)-8s %(message)s'):
        handler.setLevel(handler_level)
        formatter = logging.Formatter(handler_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logger_level)
