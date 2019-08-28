"""Module summary

Extended summary

"""

import argparse
import os
import sqlite3
import time


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


if __name__ == '__main__':
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Create SQLite database")
    parser.add_argument("-o", action="store_true", dest="overwrite",
                        default=False,
                        help="Overwrite the database file")
    parser.add_argument("-d", "--database", default="database.sqlite",
                        help="Path to the SQLite database file")
    parser.add_argument("-s", "--schema", required=True,
                        help="Path to the schema file")
    # Process command-line arguments
    args = parser.parse_args()
    # Create database
    create_db(args.overwrite, args.database, args.schema)
