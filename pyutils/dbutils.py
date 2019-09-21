"""Module that defines common database functions.

See Also
--------
pyutils.genutils : module that defines many general and useful functions.
pyutils.logutils : module that defines common logging functions.

"""

import logging
import os
import sqlite3
import time
from logging import NullHandler
# Custom modules
from pyutils.exceptions.sql import SQLSanityCheckError


logging.getLogger(__name__).addHandler(NullHandler())
logger = logging.getLogger(__name__)


def connect_db(db_path, autocommit=False):
    """Open a database connection to a SQLite database.

    Parameters
    ----------
    db_path : str
        File path to the database file.
    autocommit : bool, optional
        In autocommit mode, all changes to the database are committed as soon
        as all operations associated with the current database connection
        complete [1] (the default valud is False, which implies that statements
        that modify the database don't take effect immediately [2]. You have to
        call `commit()` to close the transaction.).

    Raises
    ------
    sqlite3.Error
        Raised if any SQLite-related errors occur, e.g. IntegrityError or
        OperationalError, since sqlite3.Error is the class for all exceptions
        of the module.

    Returns
    -------
    sqlite3.Connection
        Connection object that represents the SQLite database.

    References
    ----------
    .. [1] `7.0 Transaction Control At The SQL Level
    <https://www.sqlite.org/lockingv3.html/>`_.
    .. [2] `Controlling Transactions
    <https://docs.python.org/3/library/sqlite3.html#controlling-transactions/>`_.

    """
    # TODO: add reference
    try:
        if autocommit:
            # If isolation_level is None, it will leave the underlying sqlite3
            # library operating in autocommit mode
            # Ref.: https://bit.ly/2mg5Hie
            conn = sqlite3.connect(db_path, isolation_level=None)
        else:
            conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        raise sqlite3.Error(e)
    else:
        return conn


def create_db(overwrite_db, db_filepath, schema_filepath, **kwargs):
    """Create a SQLite database.

    A schema file is needed for creating the database. If an existing SQLite
    database will be overwritten, the user is given 5 seconds to stop the script
    before the database is overwritten.

    Parameters
    ----------
    overwrite_db : bool
        Whether the database will be overwritten. The user is given some time
        to stop the script before the database is overwritten.
    db_filepath : str
        Path to the SQLite database.
    schema_filepath : str
        Path to the schema file.
    **kwargs
        TODO

    Raises
    ------
    IOError
        Raised if there is any IOError when opening the schema file, e.g. the
        schema file doesn't exist (OSError).

    """
    db_filepath = os.path.expanduser(db_filepath)
    schema_filepath = os.path.expanduser(schema_filepath)
    db_exists = os.path.exists(db_filepath)

    if overwrite_db and db_exists:
        logger.warning("{} will be overwritten ...".format(db_filepath))
        # Exit program before delay expires or the database is overwritten
        time.sleep(5)
        os.remove(db_filepath)

    if not db_exists or overwrite_db:
        logger.info("Creating database '{}'".format(db_filepath))
        with sqlite3.connect(db_filepath) as conn:
            try:
                with open(schema_filepath, 'rt') as f:
                    schema = f.read()
                    conn.executescript(schema)
            except IOError as e:
                raise IOError(e)
            else:
                logger.info("Database created!")
    else:
        logger.warning("Database '{}' already exists!".format(db_filepath))


def sql_sanity_check(sql, values):
    """Perform sanity checks on an SQL query.

    Only SQL queries that have values to be added are checked, i.e. INSERT
    queries.

    These are the checks performed:
    * Whether the values are of the ``tuple`` type
    * Whether the SQL expression contains the right number of values

    Parameters
    ----------
    sql : str
        SQL query to be executed.
    values : tuple of str
        The values to be inserted in the database.

    Raises
    ------
    SQLSanityCheckError
        Raised when the sanity check on a SQL query fails: e.g. the query's
        values are not of `tuple` type or wrong number of values in the SQL
        query.

    """
    if type(values) is not tuple:
        raise SQLSanityCheckError(
            "[TypeError] The values for the SQL expression are not of "
            "tuple type")
    if len(values) != sql.count('?'):
        raise SQLSanityCheckError(
            "[AssertionError] Wrong number of values ({}) in the SQL "
            "expression '{}'".format(len(values), sql))
