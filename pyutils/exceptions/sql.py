"""Module that defines exceptions related to SQL database problems.

These are the exceptions that are raised when querying a SQL database.

"""


class SQLSanityCheckError(Exception):
    """Raised if one of the sanity checks on a SQL query fails: e.g. the
    query's values are not of `tuple` type or wrong number of values in the SQL
    query."""
