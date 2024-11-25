# TODO list

## Handle dates

I ran into a problem where in `rebalance_hours_raw.py` the sorting
of dates was incorrect, see [bot chat](https://chatgpt.com/share/6744bc50-c064-800c-9917-58170a0eee4b).
The short term solution was to when sorting use DATE

```
 def fetch_sorted_data_add_rowid(cursor, table_name):
     # Sort the data and add ROWID so we can
-    query = f"SELECT ROWID, * FROM {table_name} ORDER BY Name, Pay_Date"
+    query = f"SELECT ROWID, * FROM {table_name} ORDER BY Name, DATE(Pay_Date, 'localtime')"
     cursor.execute(query)
     return cursor.fetchall()
```

The long term solution is probably to change `create_table.py` in `load.py` to reformat the
date to a format that can be sorted correctly. The bot also suggested to maybe use a different
database that supports dates better.


## Handle parsing of money

Handle parsing money, short version it's complex!
https://chatgpt.com/c/6742abf0-baac-800c-8d40-d3491cc0d4de

This is a "general" version in python:

```
import locale

def parse_money(value, locale_name):
    locale.setlocale(locale.LC_ALL, locale_name)
    # Remove currency symbols and unnecessary characters
    value = ''.join(c for c in value if c.isdigit() or c in ",.")
    return locale.atof(value)
```

### Examples
us_value = parse_money("$1,234.56", "en_US.UTF-8")  # 1234.56
europe_value = parse_money("€1.234,56", "de_DE.UTF-8")  # 1234.56
india_value = parse_money("₹1,23,456.78", "en_IN.UTF-8")  # 123456.78
sweden_value = parse_money("1 234,56 kr", "sv_SE.UTF-8")  # 1234.56

