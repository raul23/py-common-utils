#!/usr/script/env python
"""Script for creating a SQLite database.

A schema file is needed for creating the database. If an existing SQLite
database will be overwritten, the user is given 5 seconds to stop the script
before the database is overwritten.

TODO: add usage

"""

import argparse

from pyutils.dbutils import create_db


# TODO: explain
PAUSE = 3


def main():
    """TODO

    Returns
    -------

    """
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Create SQLite database")
    parser.add_argument("-o", "--overwrite", action="store_true",
                        dest="overwrite", default=False,
                        help="Overwrite the database file")
    parser.add_argument("-d", "--database", default="database.sqlite",
                        help="Path to the SQLite database file")
    parser.add_argument("-s", "--schema", required=True,
                        help="Path to the schema file")
    # TODO: add verbose argument since no message is shown on the console
    # Process command-line arguments
    args = parser.parse_args()
    # Create database
    return create_db(args.database, args.schema, args.overwrite, PAUSE)


if __name__ == '__main__':
    main()
