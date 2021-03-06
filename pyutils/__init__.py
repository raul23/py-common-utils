"""Library of common Python utilities

"""


def install_colored_logger():
    """TODO

    Returns
    -------

    """
    import logging
    from pyutils.colored_logger import ColoredLogger
    # if name in logging.Logger.manager.loggerDict:
    #    del logging.Logger.manager.loggerDict[name]
    logging.Logger.manager.setLoggerClass(ColoredLogger)


def uninstall_colored_logger():
    """TODO

    Returns
    -------

    """
    # TODO: add printing with try...except like in install_colored_logger()
    import logging
    from pyutils import colored_logger

    logging.Logger.manager.setLoggerClass(logging.Logger)
    # TODO: all the existing loggers are from ColoredLogger
    # Check logging.Logger.manager.loggerDict and you will some have
    # ColoredLogger as the logger class. Right now, not a big problem.
    colored_logger._disableColoring = True


# Version of pyutils package
__version__ = "0.1"


