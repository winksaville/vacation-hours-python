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

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    if len(sys.argv) < 3:
        print("Usage: python dump_ledger.py <db_file> <table_name>")
        sys.exit(1)

    db_filename = sys.argv[1]
    table_name = sys.argv[2]
    dump_table(db_filename, table_name)
