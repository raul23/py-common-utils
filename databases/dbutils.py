"""Module summary

Extended summary

"""

import os
import sqlite3
import time


def connect_db(db_path, autocommit=False):
    """Create a database connection to a SQLite database

    Parameters
    ----------
    db_path : str
        Absolute path to database file
    autocommit : bool
        Description

    Raises
    ------
    sqlite3.Error

    Returns
    -------
    sqlite3.Connection object

    """
    try:
        if autocommit:
            conn = sqlite3.connect(db_path, isolation_level=None)
        else:
            conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        raise sqlite3.Error(e)


def create_db(overwrite, db_filepath, schema_filepath):
    """

    Parameters
    ----------
    overwrite : bool
    db_filepath : str
    schema_filepath : str

    """
    # NOTE: if you need to suppress printing, check the following links
    # - https://bit.ly/2QKRFPX
    # - https://bit.ly/2HmTIa4
    db_exists = os.path.exists(db_filepath)

    if overwrite and db_exists:
        print("WARNING: {} will be overwritten ...".format(db_filepath))
        # Exit program before delay expires or the database is overwritten
        time.sleep(5)
        os.remove(db_filepath)

    if not db_exists or overwrite:
        print("Creating database")
        with sqlite3.connect(db_filepath) as conn:
            try:
                with open(schema_filepath, 'rt') as f:
                    schema = f.read()
                    conn.executescript(schema)
            except IOError as e:
                raise IOError(e)
            else:
                print("Database created!")
    else:
        print("Database '{}' already exists!".format(args.database))
