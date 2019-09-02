"""Module that defines exceptions related to SQL database problems.

These are the exceptions that are raised when querying a SQL database.

"""


class EmptyQueryResultSetError(Exception):
    """Raised when a SQL query returns an empty result set, i.e. no rows."""


class SQLSanityCheckError(Exception):
    """Raised when the sanity check on a SQL query fails: e.g. the query's
    values are not of `tuple` type or wrong number of values in the SQL
    query."""
