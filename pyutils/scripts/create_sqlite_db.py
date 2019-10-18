#!/usr/script/env python
"""Script for creating a SQLite database.

A schema file is needed for creating the database. If an existing SQLite
database will be overwritten, the user is given 5 seconds to stop the script
before the database is overwritten.


"""

import argparse
import logging

import pyutils.dbutils as dbutils
from pyutils.dbutils import create_db
from pyutils.logutils import setup_basic_logger


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler)


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
    parser.add_argument("-sleep", type=int, default=2, help=argparse.SUPPRESS)
    parser.add_argument("-dc",  "--disable_color", action="store_true",
                        default=False, help=argparse.SUPPRESS)
    # TODO: add verbose and quiet options
    # Process command-line arguments
    args = parser.parse_args()
    # Setup logging for script
    setup_basic_logger(
        name=__name__,
        add_console_handler=True,
        handlers_to_remove=[logging.NullHandler])
    # Setup logging for create_db
    setup_basic_logger(
        name=dbutils.__name__,
        add_console_handler=True,
        handlers_to_remove=[logging.NullHandler]
    )
    dbutils.SLEEP = args.sleep
    if args.disable_color:
        # Disable coloring log messages
        dbutils.logger.disable_color()
        logger.disable_color()
    # Create database
    return create_db(args.database, args.schema, args.overwrite)


if __name__ == '__main__':
    retcode = main()
    msg = "\nScript exited with <color>{}</color>".format(retcode)
    if retcode == 1:
        logger.error(msg)
    else:
        logger.info(msg)
