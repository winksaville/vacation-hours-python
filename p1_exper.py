#!/usr/bin/env python3

# Standard library imports
import logging
import os
import sqlite3
import sys

# Local application imports
from version import version

def connect_to_db(db_name='ledger.db'):
    return sqlite3.connect(db_name)

def find_table(cursor):
    """Returns the table name if there's only one table, otherwise None."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    if len(tables) == 1:
        return tables[0]
    return None

def sort_table(db_name, table_name):
    logging.debug(f"db_name: {db_name}, table_name: {table_name}")

    # Check if the database file exists
    if not os.path.isfile(db_name):
        print(f"Database file '{db_name}' not found.")
        sys.exit(1)

    # Connect to the SQLite database
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    # If table name is not provided, try to find it automatically
    if not table_name:
        table_name = find_table(cursor)
        if not table_name:
            print("No table specified and multiple tables found in the database.")
            conn.close()
            sys.exit(1)

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if cursor.fetchone() is None:
        print(f"Table '{table_name}' does not exist in the database.")
        conn.close()
        sys.exit(1)

    # Sort the table by 'Name' and 'UniqueId'
    query = f"SELECT * FROM {table_name} ORDER BY Name, UniqueId"
    logging.debug(f"query: {query}")

    cursor.execute(query)
    rows = cursor.fetchall()

    # Fetch column names for printing
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]

    # Print sorted results
    print(f"Sorted data from table: {table_name}")
    print(f"Columns: {', '.join(columns)}")
    print("-" * 40)

    for row in rows:
        print(row)

    conn.close()
    logging.debug(f"db_name: {db_name}, table_name: {table_name} - Finished")

def usage():
    print(f"Version: {version}")
    print()
    print("Usage: ./p1_exper.py <db_filename> [table_name]")
    print("  db_filename: File name of the database")
    print("  table_name:  Optional, specify the table to process (if not provided, the app will try to find it automatically)")

if __name__ == "__main__":
    # Configure logging
    level = None
    #level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    db_filename = sys.argv[1]
    table_name = sys.argv[2] if len(sys.argv) == 3 else None

    sort_table(db_filename, table_name)
