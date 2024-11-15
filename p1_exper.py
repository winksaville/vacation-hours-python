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
    if len(tables) == 1:
        return tables[0]
    return None

def add_rebalance_column(cursor, table_name):
    """Adds 'Rebalance_hours' column if it doesn't exist."""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    if "Rebalance_hours" not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN Rebalance_hours INTEGER DEFAULT 0")
        logging.debug(f"Added 'Rebalance_hours' column to {table_name}")

def sort_and_rebalance(db_name, table_name):
    logging.debug(f"db_name: {db_name}, table_name: {table_name}")

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

    # Sort and fetch the data
    query = f"SELECT * FROM {table_name} ORDER BY Name, UniqueId"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Get the list of columns
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]

    # Index of columns
    idx_name = columns.index("Name")
    idx_hours_accrued = columns.index("Hours_accrued")
    idx_unique_id = columns.index("UniqueId")

    # Rebalance calculation
    rebalance_hours = 0
    previous_name = None

    for row in rows:
        unique_id = row[idx_unique_id]
        name = row[idx_name]
        hours_accrued = int(row[idx_hours_accrued])

        if name != previous_name:
            rebalance_hours = 0

        rebalance_hours += hours_accrued

        # Update the row with the new Rebalance_hours
        cursor.execute(
            f"UPDATE {table_name} SET Rebalance_hours = ? WHERE UniqueId = ?",
            (rebalance_hours, unique_id),
        )

        previous_name = name

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
