"""Library of common Python utilities

"""


def install_colored_logger():
    import logging
    from pyutils.colored_logger import ColoredLogger

    # if name in logging.Logger.manager.loggerDict:
    #    del logging.Logger.manager.loggerDict[name]
    logging.Logger.manager.setLoggerClass(ColoredLogger)


def uninstall_colored_logger():
    import logging
    import pyutils.colored_logger as clog

    logging.Logger.manager.setLoggerClass(logging.Logger)


# Version of pyutils package
__version__ = "1.0.0"


