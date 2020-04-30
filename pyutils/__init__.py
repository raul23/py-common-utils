"""Library of common Python utilities

"""


def install_colored_logger():
    import logging
    try:
        print("Installing the colored logger ...\n")
        from pyutils.colored_logger import ColoredLogger
    except ImportError as e:
        print(e)
        print("\nThe colored logger couldn't be installed. Install first the required package.")
        print("Fallback to simple logger\n")
    else:
        # if name in logging.Logger.manager.loggerDict:
        #    del logging.Logger.manager.loggerDict[name]
        logging.Logger.manager.setLoggerClass(ColoredLogger)


def uninstall_colored_logger():
    # TODO: add printing with try...except like in install_colored_logger()
    import logging
    from pyutils import colored_logger

    logging.Logger.manager.setLoggerClass(logging.Logger)
    # TODO: all the existing loggers are from ColoredLogger
    colored_logger._disableColoring = True


# Version of pyutils package
__version__ = "0.1"


