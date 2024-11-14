#!/usr/bin/env python3

# Standard library imports
import csv
import logging
import os
import sqlite3
import sys

# Local application imports
from version import version

def check_file_exists(csv_file):
    if not os.path.isfile(csv_file):
        print(f"File '{csv_file}' not found.")
        sys.exit(1)

def connect_to_db(db_name='ledger.db'):
    return sqlite3.connect(db_name)

def get_table_name(csv_file):
    return os.path.splitext(os.path.basename(csv_file))[0]

def sanitize_headers(headers):
    """Remove spaces and replace them with underscores in the headers."""
    return [header.strip().replace(" ", "_") for header in headers]

def get_headers_from_csv(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
    return sanitize_headers(headers)

def create_table(cursor, table_name, headers):
    logging.debug(f"table_name: {table_name}")
    logging.debug(f"headers: {headers}")
    columns = ', '.join([f'"{header}" TEXT' for header in headers])

    # Set 'UniqueId' as the primary key
    if "UniqueId" in headers:
        columns += ', PRIMARY KEY("UniqueId")'

    logging.debug(f"columns: {columns}")
    cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})')

def insert_data_from_csv(cursor, table_name, headers, csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        insert_query = f"INSERT OR IGNORE INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})"
        logging.debug(f"insert_query: {insert_query}")

        new_records_count = 0
        for row in reader:
            cursor.execute(insert_query, row)
            if cursor.rowcount > 0:
                new_records_count += 1

        return new_records_count

def load_csv_to_sqlite(db_filename, csv_filename, table_name):
    check_file_exists(csv_filename)

    conn = connect_to_db(db_filename)
    cursor = conn.cursor()

    headers = get_headers_from_csv(csv_filename)
    logging.debug(f"headers: {headers}");

    create_table(cursor, table_name, headers)
    new_records_count = insert_data_from_csv(cursor, table_name, headers, csv_filename)

    conn.commit()
    conn.close()
    print(f"Data from '{csv_filename}' loaded into '{db_filename}' as table '{table_name}'.")
    print(f"New records loaded: {new_records_count}")

def usage():
    print(f"Version: {version}")
    print()
    print("Usage: ./load.py <name> or <db_filename> <csv_filename> {table_name}")
    print("  name: If only one parameter db_filename=name.db csv_filename=name.csv table_name=name")
    print("  db_filename: Name of the database file")
    print("  csv_filename: Name of the csv file that will be added to the database")
    print("  table_name:   Optional, if not supplied it will be the basename of the csv_filename")
    print("                example; csv_filename=vacation_hours.csv table_name=vacation_hours")

if __name__ == "__main__":
    # Configure logging
    level = None
    #level = loggine.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    if len(sys.argv) == 1:
        logging.debug("len(sys.argv) == 1")
        usage()
        sys.exit(1)

    if len(sys.argv) == 2:
        table_name = sys.argv[1]
        db_filename = table_name + ".db"
        csv_filename = table_name + ".csv"
    elif len(sys.argv) == 3:
        db_filename = sys.argv[1]
        csv_filename = sys.argv[2]
        table_name = get_table_name(csv_filename)
    elif len(sys.argv) == 4:
        db_filename = sys.argv[1]
        csv_filename = sys.argv[2]
        table_name = sys.argv[3]
    else:
        logging.debug("else")
        usage()
        sys.exit(1)

    load_csv_to_sqlite(db_filename, csv_filename, table_name)
