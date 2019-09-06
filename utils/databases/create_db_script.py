"""Script for creating a SQLite database.

A schema file is needed for creating the database. If an existing SQLite
database will be overwritten, the user is given 5 seconds to stop the script
before the database is overwritten.

"""

import argparse
# Custom modules
# NOTE: `from .dbutils import create_db` not working when running the script
# with `python create_db_script.py -o -d music.sqlite -s music.sql`
# See https://stackoverflow.com/a/41817024
from dbutils import create_db


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
