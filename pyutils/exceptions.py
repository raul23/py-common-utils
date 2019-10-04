"""Module that defines exceptions ...

"""


# Connection error
class HTTP404Error(Exception):
    """Raised if the server returns a 404 status code because the webpage is
    not found."""


# Files error
class OverwriteFileError(Exception):
    """Raised if an existing file is being overwritten and the flag to
    overwrite files is disabled."""


# Logging error
class LoggingSanityCheckError(Exception):
    """Raised if the sanity check on one of the ``LoggingWrapper`` parameters
    fails."""


# SQL error
class SQLSanityCheckError(Exception):
    """Raised if one of the sanity checks on a SQL query fails: e.g. the
    query's values are not of `tuple` type or wrong number of values in the SQL
    query."""
