import argparse
# Own modules
from .logging_boilerplate import LoggingBoilerplate


# TODO: should it be a subclass of `LoggingBoilerplate` or could
# `LoggingBoilerplate` just be instantiated within?
class ScriptBoilerplate(LoggingBoilerplate):
    def __init__(self, module_name, module_file, cwd, parser_desc,
                 parser_formatter_class):
        # Setup argument parser
        self.parser = argparse.ArgumentParser(
            description=parser_desc,
            formatter_class=parser_formatter_class)
        self._setup_argparser()
        # Process command-line arguments
        self.args = self.parser.parse_args()
        super().__init__(
            module_name=module_name,
            module_file=module_file,
            logging_cfg=self.args.logging_cfg,
            cwd=cwd,
            use_default_colors=self.args.use_default_colors,
            use_pycharm_colors=self.args.use_pycharm_colors)

    def _setup_argparser(self):
        self.parser.add_argument(
            "-l", "--logging_cfg", default="logging_cfg.yaml",
            help="Path to the YAML logging configuration file.")
        self.parser.add_argument(
            "-m", "--main_cfg", default="main_cfg.yaml",
            help="Path to the YAML main configuration file.")
        # TODO: combine both options `pycharm_colors` and `use_color` into one option
        self.parser.add_argument(
            "-p", "--use_pycharm_colors",
            action='store_true',
            default=False,
            help="Use colors for the logging messages as specified for the Pycharm "
                 "Terminal. By default, we use colors for the logging messages as "
                 "defined for the standard Unix Terminal.")
        self.parser.add_argument(
            "-u", "--use_default_colors",
            action='store_true',
            default=False,
            help="Add colors to log messages. These are the default colors used "
                 "for standard Unix Terminal.")
