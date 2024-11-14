#!/usr/bin/env python3
import csv
import sqlite3
import sys
import os
import logging

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
    logging.debug(f"columns: {columns}")
    cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})')

def insert_data_from_csv(cursor, table_name, headers, csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})"
        logging.debug(f"insert_query: {insert_query}")
        for row in reader:
            cursor.execute(insert_query, row)

def load_csv_to_sqlite(csv_file):
    check_file_exists(csv_file)

    conn = connect_to_db()
    cursor = conn.cursor()

    table_name = get_table_name(csv_file)
    headers = get_headers_from_csv(csv_file)
    logging.debug(f"headers: {headers}");

    create_table(cursor, table_name, headers)
    insert_data_from_csv(cursor, table_name, headers, csv_file)

    conn.commit()
    conn.close()
    print(f"Data from '{csv_file}' loaded into 'ledger.db' as table '{table_name}'.")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    if len(sys.argv) < 2:
        print("Usage: python load_csv.py <csv_file>")
        sys.exit(1)

    csv_filename = sys.argv[1]
    load_csv_to_sqlite(csv_filename)
