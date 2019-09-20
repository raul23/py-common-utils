"""Module that defines exceptions related to logging problems.

These are the exceptions that are raised when logging.

"""


class LoggingSanityCheckError(Exception):
    """Raised if the sanity check on one of the ``LoggingWrapper`` parameters
    fails."""
