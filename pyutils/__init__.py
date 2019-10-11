"""Library of common Python utilities

"""


def install_colored_logger(name=None, terminal="UNIX"):
    import logging
    import pyutils.colored_logger as clog

    clog.TERMINAL_USED = terminal

    if name in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict[name]
    logging.Logger.manager.setLoggerClass(clog.ColoredLogger)


def change_terminal(terminal):
    import pyutils.colored_logger as clog

    clog.


# Version of pyutils package
__version__ = "1.0.0"


