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
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN Rebalance_hours REAL DEFAULT 0.0")
        logging.debug(f"Added 'Rebalance_hours' column to {table_name}")
    logging.debug(f"add_rebalance_column: columns: {columns}")

def fetch_sorted_data_add_rowid(cursor, table_name):
    # Sort the data and add ROWID so we can
    query = f"SELECT ROWID, * FROM {table_name} ORDER BY Name, DATE(Pay_Date, 'localtime')"
    cursor.execute(query)
    return cursor.fetchall()

def get_column_indices(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return {
        "Pay_Date": columns.index("Pay_Date"),
        "Name": columns.index("Name"),
        "Transaction_Amount": columns.index("Transaction_Amount"),
        "Balance": columns.index("Balance"),
        "Rebalance_hours": columns.index("Rebalance_hours"),
    }

def get_column_indices_from_query(cursor):
    # `cursor.description` contains column metadata for the most recent query
    columns = [desc[0] for desc in cursor.description]
    return {
        "rowid": columns.index("rowid") if "rowid" in columns else None,
        "Pay_Date": columns.index("Pay_Date") if "Pay_Date" in columns else None,
        "Name": columns.index("Name") if "Name" in columns else None,
        "Transaction_Amount": columns.index("Transaction_Amount") if "Transaction_Amount" in columns else None,
        "Balance": columns.index("Balance") if "Balance" in columns else None,
        "Rebalance_hours": columns.index("Rebalance_hours") if "Rebalance_hours" in columns else None,
    }

def update_rebalance_hours(connection, table_name):
    """Add rebalance column, fetch sorted data and rebalance hours."""
    logging.debug(f"update_reblance_hours:+") # row: {rows}")

    rebalance_hours = 0.0
    previous_rebalance_hours = 0.0
    previous_name = None

    cursor = connection.cursor()

    try:
        # Add the new column
        add_rebalance_column(cursor, table_name)

        # Sort the data and add rowid so we can update the row
        # as we loop through them updating rebalance_hours.
        rows = fetch_sorted_data_add_rowid(cursor, table_name)
        for row in rows:
            logging.debug(f"update_reblance_hours: TOL row: {row}")

        # Get the indices
        indices = get_column_indices_from_query(cursor)
        logging.debug(f"sort_and_rebalance: indices: {indices}")

        for row in rows:
            rowid = row[indices["rowid"]]
            pay_date = row[indices["Pay_Date"]]
            name = row[indices["Name"]]
            hours_accrued = row[indices["Transaction_Amount"]]
            balance = row[indices["Balance"]]

            logging.debug(f"update_rebalance_hours: TOL rowid: {rowid}, name: {name}, pay_date: {pay_date}, hours_accrued: {hours_accrued}, balance: {balance}")

            if name != previous_name:
                # Initialize previous_rebalance_hours to 0 as this
                # is the first entry for a new set of names.
                logging.debug(f"update_reblance_hours: new name: {name} previous_name: {previous_name}")
                previous_rebalance_hours = 0

            # Get the Rebalance_hours and update only if it's 0.
            # If it's not zero than this has already been processed
            # and we don't want to do it again.
            rebalance_hours = float(row[indices["Rebalance_hours"]])
            if rebalance_hours == 0:
                logging.debug(f"update_reblance_hours: rebalance_hours: {rebalance_hours} == 0")
                # We ignore negative hours_accured while calculating rebalance_hours
                # so rebalance_hours converges to balance more evenly and
                # quickly.
                if hours_accrued >= 0:
                    # if positive update rebalance_hours
                    logging.debug(f"update_reblance_hours: inc rebalance_hours: {rebalance_hours} by  hours_accrued: {hours_accrued}")
                    rebalance_hours = previous_rebalance_hours + hours_accrued
                else:
                    # If negative inherit the previous value
                    logging.debug(f"update_reblance_hours: set rebalance_hours: {rebalance_hours} to {previous_rebalance_hours}")
                    rebalance_hours = previous_rebalance_hours

                # We've updated rebalance_hours but it must never exceed balance,
                # which is the current actual number of vacation hours accrued. This
                # means that once rebalance reaches balance it will remain
                # in equalibrium and never diverge.
                if rebalance_hours > balance:
                    logging.debug(f"update_reblance_hours: set rebalance_hours: {rebalance_hours} to {balance}")
                    rebalance_hours = balance
                logging.debug(f"update_reblance_hours: rebalance_hours: {rebalance_hours}")

                #cursor.execute(
                #    f"UPDATE {table_name} SET Rebalance_hours = ? WHERE Pay_Date = ?",
                #    (rebalance_hours, pay_date)
                #)
                cursor.execute(
                    f"UPDATE {table_name} SET Rebalance_hours = {rebalance_hours} WHERE ROWID = {rowid}")
            else:
                logging.debug(f"update_reblance_hours: rebalance_hours: {rebalance_hours} != 0,  ignore because we've updated in a previous run!")


            previous_name = name
            previous_rebalance_hours = rebalance_hours
            logging.debug(f"update_reblance_hours: BOL rebalance_hours: {rebalance_hours} previous_rebalance_hours: {previous_rebalance_hours} previous_name: {previous_name}")

    finally:
        cursor.close()

    logging.debug(f"update_reblance_hours:-") # row: {rows}")

def print_table_data(connection, table_name):
    """Prints the contents of the table in a formatted way."""
    temp_cursor = connection.cursor()  # Explicitly create a new cursor
    try:
        # Fetch column names
        temp_cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [info[1] for info in temp_cursor.fetchall()]

        # Fetch all data from the table
        temp_cursor.execute(f"SELECT * FROM {table_name}")
        rows = temp_cursor.fetchall()

        # Print the table name and columns
        print(f"Table: {table_name}")
        print(f"Columns: {', '.join(columns)}")
        print("-" * 40)

        # Print each row
        for row in rows:
            print(row)

        print("-" * 40)
        print(f"Total rows: {len(rows)}")
    finally:
        temp_cursor.close()  # Ensure the cursor is closed

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

    logging.debug(f"sort_and_rebalance: print_table_data before update_rebalance");
    print_table_data(conn, table_name)


    update_rebalance_hours(conn, table_name)
    logging.debug(f"sort_and_rebalance: print_table_data after update_rebalance");
    print_table_data(conn, table_name)

    conn.commit()
    conn.close()
    print(f"Rebalance hours updated for table '{table_name}'.")

def usage():
    print(f"Version: {version}")
    print()
    print("Usage: ./p1_exper.py <name> or <db_filename> <table_name>")
    print("  name: If only one parameter db_filename=name.db table_name=name")
    print("  db_filename: File name of database")
    print("  table_name: Table within the database to dump")


if __name__ == "__main__":
    level = None
    #level = logging.DEBUG
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

    sort_and_rebalance(db_filename, table_name)
