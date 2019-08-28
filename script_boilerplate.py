"""Module summary

Extended module summary

"""

import argparse
# Custom modules
from utilities.custom_logging.logging_boilerplate import LoggingBoilerplate


class ScriptBoilerplate:
    """

    Parameters
    ----------
    module_name
    module_file
    cwd
    parser_desc
    parser_formatter_class
    """
    # TODO: add configuration filenames/short and long names options in
    # `__init__()`
    def __init__(self, module_name, module_file, cwd, parser_desc,
                 parser_formatter_class):
        self.module_name = module_name
        self.module_file = module_file
        self.cwd = cwd
        # Setup argument parser
        self.parser = argparse.ArgumentParser(
            description=parser_desc,
            formatter_class=parser_formatter_class)
        self._add_init_arguments()
        self.lb = None
        self.args = None
        self.logging_cfg_dict = None

    def _add_init_arguments(self):
        """

        """
        self.parser.add_argument(
            "-l", "--logging_cfg", default="logging_cfg.yaml",
            help="Path to the YAML logging configuration file.")
        self.parser.add_argument(
            "-m", "--main_cfg", default="main_cfg.yaml",
            help="Path to the YAML main configuration file.")
        self.parser.add_argument(
            "-p", "--use_pycharm_colors",
            action='store_true',
            default=False,
            help="Use colors for the logging messages as specified for the "
                 "Pycharm Terminal. By default, we use colors for the logging "
                 "messages as defined for the standard Unix Terminal.")
        self.parser.add_argument(
            "-u", "--use_default_colors",
            action='store_true',
            default=False,
            help="Add colors to log messages. These are the default colors used "
                 "for standard Unix Terminal.")

    def add_argument(self, **kwargs):
        """

        Parameters
        ----------
        kwargs


        """
        self.parser.add_argument(**kwargs)

    def get_logger(self):
        """

        Returns
        -------

        """
        return self.lb.get_logger()

    def parse_args(self):
        """Parse command-line arguments

        """
        self.args = self.parser.parse_args()
        self.lb = LoggingBoilerplate(
            module_name=self.module_name,
            module_file=self.module_file,
            logging_cfg=self.args.logging_cfg,
            cwd=self.cwd,
            use_default_colors=self.args.use_default_colors,
            use_pycharm_colors=self.args.use_pycharm_colors)
        self.logging_cfg_dict = self.lb.logging_cfg_dict
