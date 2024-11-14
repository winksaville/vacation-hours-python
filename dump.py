#!/usr/bin/env python3
import sqlite3
import sys
import os
import logging

def dump_table(db_name, table_name):
    logging.debug(f"db_name: {db_name} table_name: {table_name}:+");

    # Check if the database file exists
    if not os.path.isfile(db_name):
        print(f"Database file '{db_name}' not found.")
        sys.exit(1)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if cursor.fetchone() is None:
        print(f"Table '{table_name}' does not exist in the database.")
        conn.close()
        sys.exit(1)

    # Fetch and display the table contents
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Fetch column names for printing
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    print(f"Table: {table_name}")
    print(f"Columns: {', '.join(columns)}")
    print("-" * 40)

    # Print each row
    for row in rows:
        print(row)

    conn.close()
    logging.debug(f"db_name: {db_name} table_name: {table_name}:-");

def usage():
    print("Usage: ./dump.py <name> or <db_filename> <table_name>")
    print("  name: If only one parameter db_filename=name.db table_name=name")
    print("  db_filename: File name of database")
    print("  table_name: Table within the database to dump")

if __name__ == "__main__":
    # Configure logging
    level = None
    #level = loggine.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    if len(sys.argv) == 2:
        table_name = sys.argv[1]
        db_filename = table_name + ".db"
    elif len(sys.argv) == 3:
        db_filename = sys.argv[1]
        table_name = sys.argv[2]
    else:
        usage()
        sys.exit(1)

    dump_table(db_filename, table_name)
