"""Module that defines exceptions ...

"""


# Connection error
class HTTP404Error(Exception):
    """Raised if the server returns a 404 status code because the webpage is
    not found."""


# SQL error
# IMPORTANT
# TODO: remove this error and its usage in dbutils.sql_sanity_check and
# lyrics_scraping.scrapers.lyrics_scraping
class SQLSanityCheckError(Exception):
    """Raised if one of the sanity checks on a SQL query fails: e.g. the
    query's values are not of `tuple` type or wrong number of values in the SQL
    query."""
