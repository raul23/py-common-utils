"""Module that defines common database functions.

See Also
--------
genutils : module that defines many general and useful functions.
logutils : module that defines common logging functions.

"""

import logging
import os
import sqlite3
import time

from pyutils.exceptions import SQLSanityCheckError
from pyutils.logutils import get_error_msg


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler)


# TODO
SLEEP = 2


def connect_db(db_path, autocommit=False):
    """Open a database connection to a SQLite database.

    Parameters
    ----------
    db_path : str
        File path to the database file.
    autocommit : bool, optional
        In autocommit mode, all changes to the database are committed as soon
        as all operations associated with the current database connection
        complete [1]_ (the default value is False which implies that statements
        that modify the database don't take effect immediately [2]_. You have to
        call :meth:`~sqlite3.Connection.commit` to close the transaction.).

    Raises
    ------
    sqlite3.Error
        Raised if any SQLite-related errors occur, e.g. :exc:`IntegrityError` or
        :exc:`OperationalError`, since :exc:`sqlite3.Error` is the class for all
        exceptions of the module.

    Returns
    -------
    sqlite3.Connection
        Connection object that represents the SQLite database.

    .. [1] `7.0 Transaction Control At The SQL Level
       <https://www.sqlite.org/lockingv3.html>`_.
    .. [2] `Controlling Transactions (Python docs)
       <https://bit.ly/2mg5Hie>`_.

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
    except sqlite3.Error:
        raise
    else:
        return conn


def create_db(db_filepath, schema_filepath, overwrite_db=False, **kwargs):
    """Create a SQLite database.

    A schema file is needed for creating the database.

    Parameters
    ----------
    db_filepath : str
        Path to the SQLite database.
    schema_filepath : str
        Path to the schema file.
    overwrite_db : bool, optional
        Whether the database will be overwritten. The user is given some time
        to stop the script before the database is overwritten (the default value
        is False which means the db will not be overwritten).
    **kwargs
        TODO

    Returns
    -------
    int
        Return code. TODO ...

    Raises
    ------
    IOError
        Raised if there is any IOError when opening the schema file, e.g. the
        schema file doesn't exist (OSError).
    sqlite3.OperationalError
        Raised if TODO ...

    """
    # TODO: add verbose
    db_filepath = os.path.expanduser(db_filepath)
    schema_filepath = os.path.expanduser(schema_filepath)
    db_exists = os.path.exists(db_filepath)

    if overwrite_db and db_exists:
        logger.warning(
            "<color>{} will be overwritten ...</color>".format(db_filepath))
        # TODO: ask user to confirm and emit signal after 5 seconds to stop the
        # program if no answer is given
        #
        # Exit program before delay expires or the database is overwritten
        time.sleep(SLEEP)
        os.remove(db_filepath)

    if not db_exists or overwrite_db:
        status = 1
        try:
            with sqlite3.connect(db_filepath) as conn:
                f = open(schema_filepath, 'rt')
                schema = f.read()
                conn.executescript(schema)
                f.close()
        except IOError as e:
            logger.error("<color>{}</color>".format(get_error_msg(e)))
        except sqlite3.OperationalError as e:
            logger.error("<color>{}</color>".format(get_error_msg(e)))
        else:
            logger.info("<color>Database created!</color>")
            status = 0
        finally:
            return status
    else:
        logger.warning(
            "<color>Database '{}' already exists!</color>".format(db_filepath))
        return 1


def sql_sanity_check(sql, values):
    """Perform sanity checks on an SQL query.

    Only SQL queries that have values to be added are checked, i.e. `INSERT`
    queries.

    These are the checks performed:

    - Whether the values are of :obj:`tuple` type
    - Whether the SQL expression contains the right number of values

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
        values are not of :obj:`tuple` type or wrong number of values in the SQL
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
