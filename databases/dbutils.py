"""Module summary

Extended summary

"""

import os
import sqlite3
import time
# Custom modules
from utilities.exceptions.sql import SQLSanityCheckError
from utilities.logging.logutils import get_logger


def connect_db(db_path, autocommit=False):
    """Open a database connection to a SQLite database

    Parameters
    ----------
    db_path : str
        Absolute path to database file
    autocommit : bool
        Description

    Raises
    ------
    sqlite3.Error
        Raised if any SQLite-related errors occur, e.g. IntegrityError or
        OperationalError, since sqlite3.Error is the class for all exceptions
        of the module. See

    Returns
    -------
    sqlite3.Connection object
        Description

    References
    ----------


    """
    try:
        if autocommit:
            conn = sqlite3.connect(db_path, isolation_level=None)
        else:
            conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        raise sqlite3.Error(e)


def create_db(overwrite, db_filepath, schema_filepath, logging_cfg=None):
    """

    Parameters
    ----------
    overwrite : bool
        Description
    db_filepath : str
        Description
    schema_filepath : str
        Description
    logging_cfg : dict, optional
        Description

    Raises
    ------
    IOError
        Raised if

    """
    # NOTE: if you need to suppress printing, check the following links
    # - https://bit.ly/2QKRFPX
    # - https://bit.ly/2HmTIa4
    # Setup logging
    # TODO: sanity check type of `logging_cfg`
    logger = get_logger(__name__, __file__, os.getcwd(), logging_cfg)
    db_exists = os.path.exists(db_filepath)

    if overwrite and db_exists:
        logger.warning("{} will be overwritten ...".format(db_filepath))
        # Exit program before delay expires or the database is overwritten
        time.sleep(5)
        os.remove(db_filepath)

    if not db_exists or overwrite:
        logger.info("Creating database {}".format(db_filepath))
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


def sql_sanity_check(sql, val):
        """

        Parameters
        ----------
        sql : str
            Description
        val : tuple of str
            Description

        Raises
        ------
        SQLSanityCheckError
            Raised when the sanity check on a SQL query fails: e.g. the query's
            values are not of `tuple` or wrong number of values in the SQL
            query.

            This is a custom exception.

        """
        if type(val) is not tuple:
            raise SQLSanityCheckError(
                "[TypeError] The values for the SQL expression are not of "
                "`tuple` type")
        if len(val) != sql.count('?'):
            raise SQLSanityCheckError(
                "[AssertionError] Wrong number of values ({}) in the SQL "
                "expression '{}'".format(len(val), sql))
