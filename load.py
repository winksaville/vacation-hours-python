#!/usr/bin/env python3

# Standard library imports
import csv
import logging
import os
import sqlite3
import sys
import re
from datetime import datetime

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

def infer_sqlite_type(sample_values):
    """
    Infer SQLite data type based on a list of sample values.
    """
    for value in sample_values:
        value = value.strip()
        if value.isdigit():
            logging.debug(f"INTEGER: {value}")
            return "INTEGER"
        try:
            float(value)
            logging.debug(f"REAL: {value}")
            return "REAL"
        except ValueError:
            pass
        try:
            # Check for date in MM/DD/YYYY format
            datetime.strptime(value, "%m/%d/%Y")
            logging.debug(f"DATE: {value}")
            return "DATE"
        except ValueError:
            pass
        # Check for dollar amounts (e.g., $50.00)
        if re.match(r"^\$\d+(\.\d{1,2})?$", value):
            logging.debug(f"REAL$: {value}")
            return "REAL"
    logging.debug(f"TEXT")
    return "TEXT"

def get_sample_values(csv_file, column_index, sample_size=10):
    """
    Get sample values from a specific column of the CSV file for type inference.
    """
    sample_values = []
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for i, row in enumerate(reader):
            if i >= sample_size:
                break
            sample_values.append(row[column_index])
    return sample_values

def create_table(cursor, table_name, headers, csv_file):
    """
    Create a table with inferred column types.
    """
    column_definitions = []
    for idx, header in enumerate(headers):
        sample_values = get_sample_values(csv_file, idx)
        column_type = infer_sqlite_type(sample_values)
        column_definitions.append(f'"{header}" {column_type}')

    logging.debug(f"column_definitions: {column_definitions}")

    ## Set 'UniqueId' as the primary key if it exists
    #if "UniqueId" in headers:
    #    column_definitions.append('PRIMARY KEY("UniqueId")')

    columns = ', '.join(column_definitions)
    logging.debug(f"columns: {columns}")
    query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})'
    logging.debug(f"query: {query}")
    cursor.execute(query)

def insert_data_from_csv(cursor, table_name, headers, csv_file):
    """
    Insert data into the table, converting values to match their inferred types.
    """
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        insert_query = f"INSERT OR IGNORE INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})"

        new_records_count = 0
        for row in reader:
            # Convert dollar amounts and remove the $ sign
            row = [float(value[1:]) if re.match(r"^\$\d+(\.\d{1,2})?$", value.strip()) else value.strip() for value in row]
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

    create_table(cursor, table_name, headers, csv_filename)
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
    #level = logging.DEBUG
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
