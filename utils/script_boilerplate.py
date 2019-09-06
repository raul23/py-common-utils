"""Module that allows you to setup your script for argument parsing and logging.

The module takes care of setting up the argument parser along with its default
arguments, and logging.

Examples
--------
A template on how to use this module in you script is as follows:
1. Instantiate the ``ScriptBoilerplate`` class:
>>> sb = ScriptBoilerplate(
        module_name=__name__,
        module_file=__file__,
        cwd=os.getcwd(),
        script_desc="Blabla",
        parser_formatter_class=argparse.ArgumentDefaultsHelpFormatter)
2. Parse the arguments:
>>> sb.parse_args()
3. Get the logger:
>>> logger = sb.get_logger()

You are now ready to go! You can use `logger` in the rest of your script:
>>> logger.info("Testing")

Note that `logger` is of type ``LoggingWrapper`` and is defined in
`logging_wrapper.py <https://bit.ly/2kuU1HO>`_

The reason for wrapping ``logging.Logger`` is that we add color to logs.

"""

import argparse
# Custom modules
from utils.logging.logging_boilerplate import LoggingBoilerplate


class ScriptBoilerplate:
    """Class that parses arguments from the command-line and setups logging for
    the script.

    Parameters
    ----------
    module_name : str
        Name of the module, e.g. ``'utilities.databases.dbutils'``
    module_file : str
        Module's filename, e.g. `run_scraper.py`
    cwd : str
        Module's current working directory, e.g. `.../lyrics-scraper/script`
    script_desc : str
        The string describing the program usage [1].
    parser_formatter_class : argparse.HelpFormatter
        A class for customizing the help output [1], e.g.
        ``argparse.ArgumentDefaultsHelpFormatter`` which automatically adds
        information about argument default values [2].

    References
    ----------
    .. [1] `ArgumentParser objects
    <https://docs.python.org/2/library/argparse.html#argumentparser-objects>`_.
    .. [2] `formatter_class
    <https://docs.python.org/2/library/argparse.html#formatter-class>`_.

    """
    def __init__(self, module_name, module_file, cwd, script_desc,
                 parser_formatter_class):
        # TODO: add configuration filenames/short and long names options
        self.module_name = module_name
        self.module_file = module_file
        self.cwd = cwd
        # Setup argument parser
        self.parser = argparse.ArgumentParser(
            description=script_desc,
            formatter_class=parser_formatter_class)
        self._add_default_arguments()
        self.lb = None
        self.args = None
        self.logging_cfg_dict = None

    def _add_default_arguments(self):
        """Add default arguments to the program.

        All default arguments are optional and refer to the logging YAML
        configuration file, the main YAML configuration file, and adding color
        to log messages.

        Notes
        -----
        The reason for treating separately the two different types of terminal
        is that the PyCharm terminal will display color levels differently than
        the standard Unix terminal. See `logging_wrapper.py` [1] (in the module
        description) for more info about adding color to log messages.

        References
        ----------
        .. [1] `logging_wrapper.py <https://bit.ly/2kuU1HO>`_.

        """
        self.parser.add_argument(
            "-l", "--logging_cfg", default="logging_cfg.yaml",
            help="Path to the YAML logging configuration file.")
        self.parser.add_argument(
            "-m", "--main_cfg", default="main_cfg.yaml",
            help="Path to the YAML main configuration file.")
        self.parser.add_argument(
            "-c", "--color_logs",
            const="u",
            nargs='?',
            default=None,
            choices=["u", "p"],
            help="Add colors to log messages. By default, we use colors as "
                 "defined for the standard Unix Terminal ('u'). If working with "
                 "the PyCharm terminal, use the option 'p' to get better "
                 "colors suited for this type of terminal.")

    def add_argument(self, *args, **kwargs):
        """Add a command-line argument to the program.

        Positional optional arguments can be passed to this method.

        When adding argument, the short and long names of the arguments are
        given as ``*args``.

        Parameters
        ----------
        *args : tuple
            Variable length argument tuple. The tuple contains a series of
            flags, or a simple argument name.
            For example,
            `*("-d", "--database",)` which specifies the shot and long names of
            the argument.
        **kwargs : dict
            The dictionary contains any keyword argument associated with the
            positional or optional argument.
            For example,
            ``**{"default": "database.sqlite",
                 "help": "Path to the SQLite database file"}``

            See [1] for a list of these ``**kwargs``, and their detailed
            descriptions.

        References
        ----------
        .. [1] `The add_argument() method <https://bit.ly/2m288os>`_.

        """
        self.parser.add_argument(*args, **kwargs)

    def get_logger(self):
        """Return the logger to be used in the script.

        Returns
        -------
        logger : LoggingWrapper
            The logger which is a wrapper around `logging.Logger` in order to
            give it the capability of adding color to logs.

        """
        return self.lb.get_logger()

    def parse_args(self):
        """Parse command-line arguments.

        It parses the command-line arguments (default and custom ones) and
        setups the logger.

        """
        self.args = self.parser.parse_args()
        self.lb = LoggingBoilerplate(
            module_name=self.module_name,
            module_file=self.module_file,
            logging_cfg=self.args.logging_cfg,
            cwd=self.cwd,
            color_logs=self.args.color_logs,)
        self.logging_cfg_dict = self.lb.logging_cfg_dict
