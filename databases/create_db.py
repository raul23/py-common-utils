"""Module summary

Extended summary

"""

import argparse
# Custom modules
from .dbutils import create_db


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
