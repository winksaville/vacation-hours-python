# Vacation hours

Process Vacation hours using Python

## Run

Assumes the current directory is the directory
where this repo was cloned to.

### Remove database

```
$ rm *.db
```

### Load database

Pass no parameters to see usage help `load.py`:
```
$ ./load.py
Version: 0.1.0

Usage: ./load.py <name> or <db_filename> <csv_filename> {table_name}
  name: If only one parameter db_filename=name.db csv_filename=name.csv table_name=name
  db_filename: Name of the database file
  csv_filename: Name of the csv file that will be added to the database
  table_name:   Optional, if not supplied it will be the basename of the csv_filename
                example; csv_filename=vacation_hours.csv table_name=vacation_hours
```

Pass one parameter, name
```
$ rm *.db
$ ./load.py vacation_hours
Data from 'vacation_hours.csv' loaded into 'vacation_hours.db' as table 'vacation_hours'.
New records loaded: 5
```

Pass two parameter, db_filename and csv_filename:
```
$ rm *.db
$ ./load.py ledger.db vacation_hours.csv
Data from 'vacation_hours.csv' loaded into 'ledger.db' as table 'vacation_hours'.$ ./load.py ledger.db vacation_hours.csv
New records loaded: 5
```

Here we'll use 3 parameters and load two csv files which overlap:
```
$ cat vacation_hours.name1-3.csv
UniqueId,Name,Max vacation hours,Hourly wage,Transaction date,Hours accrued,Balance hours
1,Name1,100,50,2024-10-01,8,102
2,Name1,100,50,2024-10-01,-2,100
3,Name2,50,75,2024-10-01,5,55
$ cat vacation_hours.name3-5.csv
UniqueId,Name,Max vacation hours,Hourly wage,Transaction date,Hours accrued,Balance hours
3,Name2,50,75,2024-10-01,5,55
4,Name3,200,25,2024-10-01,8,208
5,Name3,200,25,2024-10-01,-8,200
```

Here we load 3 records form `vacation_hours.name1-3.csv` and
we see 3 records:
```
$ rm *.db
$ ./load.py ledger.db vacation_hours.name1-3.csv vacation_hours
Data from 'vacation_hours.name1-3.csv' loaded into 'ledger.db' as table 'vacation_hours'.
New records loaded: 3
$ ./dump.py ledger.db vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours
----------------------------------------
('1', 'Name1', '100', '50', '2024-10-01', '8', '102')
('2', 'Name1', '100', '50', '2024-10-01', '-2', '100')
('3', 'Name2', '50', '75', '2024-10-01', '5', '55')
```

Next we'll load vacation_hours.name3-5.csv which also has
3 records, but one of the records is already present so
it's ignored and "New records loaded: 2" instead of 3:
```
$ ./load.py ledger.db vacation_hours.name3-5.csv vacation_hours
Data from 'vacation_hours.name3-5.csv' loaded into 'ledger.db' as table 'vacation_hours'.
New records loaded: 2
$ ./dump.py ledger.db vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours
----------------------------------------
('1', 'Name1', '100', '50', '2024-10-01', '8', '102')
('2', 'Name1', '100', '50', '2024-10-01', '-2', '100')
('3', 'Name2', '50', '75', '2024-10-01', '5', '55')
('4', 'Name3', '200', '25', '2024-10-01', '8', '208')
('5', 'Name3', '200', '25', '2024-10-01', '-8', '200')
```

### Dump database

Pass no parameters to see usage help `dump.py`:
```
$ ./dump.py
Version: 0.1.0

Usage: ./dump.py <name> or <db_filename> <table_name>
  name: If only one parameter db_filename=name.db table_name=name
  db_filename: File name of database
  table_name: Table within the database to dump
```

Pass one parameter and the following are used:
  - db_filename = name.db
  - table_name = name
```
$ rm *.db
$ ./load.py vacation_hours
Data from 'vacation_hours.csv' loaded into 'vacation_hours.db' as table 'vacation_hours'.
$ ./dump.py vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours
----------------------------------------
('1', 'Name1', '100', '50', '2024-10-01', '8', '102')
('2', 'Name1', '100', '50', '2024-10-01', '-2', '100')
('3', 'Name2', '50', '75', '2024-10-01', '5', '55')
('4', 'Name3', '200', '25', '2024-10-01', '8', '208')
('5', 'Name3', '200', '25', '2024-10-01', '-8', '200')
```

Pass two parameter, db_filename and table_name:
```
$ rm *.db
$ ./load.py ledger.db vacation_hours.csv
Data from 'vacation_hours.csv' loaded into 'ledger.db' as table 'vacation_hours'.
$ ./dump.py ledger.db vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours
----------------------------------------
('1', 'Name1', '100', '50', '2024-10-01', '8', '102')
('2', 'Name1', '100', '50', '2024-10-01', '-2', '100')
('3', 'Name2', '50', '75', '2024-10-01', '5', '55')
('4', 'Name3', '200', '25', '2024-10-01', '8', '208')
('5', 'Name3', '200', '25', '2024-10-01', '-8', '200')
```

### Processing 1 experiment

Computes a "Rebalance_hours" as an additional column.

ATM I think there are two corner case bugs:
  1. Rebalance_hours needs to be reduced when it exceeds
    Max_vacation_hours. Not sure how to do this as it
    as the way it's handled for Balance_hours is to
    create a new transaction. Not sure how to do that
    should we add a new transaction and change UniqueId?
  1. Correction transactions should always be ignored
    when computing Rebalance_hours. Any correction will
    be handled by 1 above.

```
$ rm *.db
$ ./p1_exper.py
Version: 0.2.0-wip

Usage: ./p1_exper.py <name> or <db_filename> <table_name>
  name: If only one parameter db_filename=name.db table_name=name
  db_filename: File name of database
  table_name: Table within the database to dump
$ ./load.py vacation_hours
Data from 'vacation_hours.csv' loaded into 'vacation_hours.db' as table 'vacation_hours'.
New records loaded: 5
$ ./dump.py vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours
----------------------------------------
('1', 'Name1', '100', '50', '2024-10-01', '8', '102')
('2', 'Name1', '100', '50', '2024-10-01', '-2', '100')
('3', 'Name2', '50', '75', '2024-10-01', '5', '55')
('4', 'Name3', '200', '25', '2024-10-01', '8', '208')
('5', 'Name3', '200', '25', '2024-10-01', '-8', '200')
$ ./p1_exper.py vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours, Rebalance_hours
----------------------------------------
('1', 'Name1', '100', '50', '2024-10-01', '8', '102', 8)
('2', 'Name1', '100', '50', '2024-10-01', '-2', '100', 6)
('3', 'Name2', '50', '75', '2024-10-01', '5', '55', 5)
('4', 'Name3', '200', '25', '2024-10-01', '8', '208', 8)
('5', 'Name3', '200', '25', '2024-10-01', '-8', '200', 0)
----------------------------------------
Total rows: 5
Rebalance hours updated for table 'vacation_hours'.
```

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.
