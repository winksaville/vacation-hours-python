#!/usr/bin/env python3

import logging
import os
import sqlite3
import sys
from version import version

def connect_to_db(db_name='ledger.db'):
    return sqlite3.connect(db_name)

def find_table(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    return tables[0] if len(tables) == 1 else None

def add_rebalance_column(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    if "Rebalance_hours" not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN Rebalance_hours INTEGER DEFAULT 0")
        logging.debug(f"Added 'Rebalance_hours' column to {table_name}")

def fetch_sorted_data(cursor, table_name):
    query = f"SELECT * FROM {table_name} ORDER BY Name, UniqueId"
    cursor.execute(query)
    return cursor.fetchall()

def get_column_indices(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return {
        "UniqueId": columns.index("UniqueId"),
        "Name": columns.index("Name"),
        "Hours_accrued": columns.index("Hours_accrued")
    }

def update_rebalance_hours(cursor, table_name, rows, indices):
    rebalance_hours = 0
    previous_name = None

    for row in rows:
        unique_id = row[indices["UniqueId"]]
        name = row[indices["Name"]]
        hours_accrued = int(row[indices["Hours_accrued"]])

        if name != previous_name:
            rebalance_hours = 0

        rebalance_hours += hours_accrued
        cursor.execute(
            f"UPDATE {table_name} SET Rebalance_hours = ? WHERE UniqueId = ?",
            (rebalance_hours, unique_id)
        )

        previous_name = name

def print_table_data(cursor, table_name):
    """Prints the contents of the table in a formatted way."""
    # Fetch column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]

    # Fetch all data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Print the table name and columns
    print(f"Table: {table_name}")
    print(f"Columns: {', '.join(columns)}")
    print("-" * 40)

    # Print each row
    for row in rows:
        print(row)

    print("-" * 40)
    print(f"Total rows: {len(rows)}")

def sort_and_rebalance(db_name, table_name):
    if not os.path.isfile(db_name):
        print(f"Database file '{db_name}' not found.")
        sys.exit(1)

    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    if not table_name:
        table_name = find_table(cursor)
        if not table_name:
            print("No table specified and multiple tables found in the database.")
            conn.close()
            sys.exit(1)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if cursor.fetchone() is None:
        print(f"Table '{table_name}' does not exist in the database.")
        conn.close()
        sys.exit(1)

    add_rebalance_column(cursor, table_name)
    rows = fetch_sorted_data(cursor, table_name)
    indices = get_column_indices(cursor, table_name)
    update_rebalance_hours(cursor, table_name, rows, indices)
    print_table_data(cursor, table_name)

    conn.commit()
    conn.close()
    print(f"Rebalance hours updated for table '{table_name}'.")

def usage():
    print(f"Version: {version}")
    print()
    print("Usage: ./p1_exper.py <db_filename> [table_name]")
    print("  db_filename: File name of the database")
    print("  table_name:  Optional, specify the table to process (if not provided, the app will try to find it automatically)")

if __name__ == "__main__":
    level = None
    #level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    db_filename = sys.argv[1]
    table_name = sys.argv[2] if len(sys.argv) == 3 else None

    sort_and_rebalance(db_filename, table_name)
