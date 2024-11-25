# Vacation hours

Process Vacation hours using Python

## Install git if git is not installed

### Git for Windows

* Download the install executable from [git-scm.com](https://git-scm.com/downloads/win)
  it says "Click here to download"
* Run `Git-x.x.x.x-64-bit.exe` in the browser you should be able to run it from the download icon
* I took the defaults, except I selected all the optional features and I use VIM as my editor.

It should be installed in `C:\Program Files\Git` and the `git.exe` should be installed.

#### Open a Git Bash shell

* Double click on the "GIT Bash" desktop icon and a command line terminal will open.
* Create a directory for the project and clone the project:
  ```
  $ mkdir -p ~/prgs/katrina
  $ cd ~/prgs/katrina
  $ git clone https://github.com/winksaville/vacation-hours-python.git
  ```
* Change to the directory where the project was cloned:
  ```
  $ cd vacation-hours-python
  ```
* Now you can run the scripts as described below.

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
Version: 0.2.0

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
New records loaded: 8
```

Pass two parameter, db_filename and csv_filename:
```
$ rm *.db
$ ./load.py ledger.db vacation_hours.csv
Data from 'vacation_hours.csv' loaded into 'ledger.db' as table 'vacation_hours'.
New records loaded: 8
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
(1, 'Name1', 100, 50, '2024-10-01', 8, 102)
(2, 'Name1', 100, 50, '2024-10-01', -2, 100)
(3, 'Name2', 50, 75, '2024-10-01', 5, 55)
```

Next we'll load vacation_hours.name3-5.csv which also has
3 records, but one of the records is already present so
it's ignored and "New records loaded: 2" instead of 3:
```
$ ./load.py ledger.db vacation_hours.name3-5.csv vacation_hours
Data from 'vacation_hours.name3-5.csv' loaded into 'ledger.db' as table 'vacation_hours'.
New records loaded: 3
$ ./dump.py ledger.db vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours
----------------------------------------
(1, 'Name1', 100, 50, '2024-10-01', 8, 102)
(2, 'Name1', 100, 50, '2024-10-01', -2, 100)
(3, 'Name2', 50, 75, '2024-10-01', 5, 55)
(3, 'Name2', 50, 75, '2024-10-01', 5, 55)
(4, 'Name3', 200, 25, '2024-10-01', 8, 208)
(5, 'Name3', 200, 25, '2024-10-01', -8, 200)
```

### Dump database

Pass no parameters to see usage help `dump.py`:
```
$ ./dump.py
Version: 0.2.0

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
New records loaded: 8
$ ./dump.py vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours
----------------------------------------
(1, 'Name1', 100.0, 50.0, '10/1/2024', 8.0, 102.0)
(2, 'Name1', 100.0, 50.0, '10/1/2024', -2.0, 100.0)
(3, 'Name2', 50.0, 75.0, '10/1/2024', 5.0, 55.0)
(4, 'Name3', 200.0, 25.0, '10/1/2024', 8.0, 25.0)
(5, 'Name1', 100.0, 50.0, '10/15/2024', 8.0, 108.0)
(6, 'Name1', 100.0, 50.0, '10/15/2024', -8.0, 100.0)
(7, 'Name2', 50.0, 75.0, '10/15/2024', 8.0, 63.0)
(8, 'Name3', 200.0, 25.0, '10/15/2024', 8.0, 33.0)
```

Pass two parameter, db_filename and table_name:
```
$ rm *.db
$ ./load.py vacation_hours^C
$ ./load.py ledger.db vacation_hours.csv
Data from 'vacation_hours.csv' loaded into 'ledger.db' as table 'vacation_hours'.
New records loaded: 8
$ ./dump.py ledger.db vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours
----------------------------------------
(1, 'Name1', 100.0, 50.0, '10/1/2024', 8.0, 102.0)
(2, 'Name1', 100.0, 50.0, '10/1/2024', -2.0, 100.0)
(3, 'Name2', 50.0, 75.0, '10/1/2024', 5.0, 55.0)
(4, 'Name3', 200.0, 25.0, '10/1/2024', 8.0, 25.0)
(5, 'Name1', 100.0, 50.0, '10/15/2024', 8.0, 108.0)
(6, 'Name1', 100.0, 50.0, '10/15/2024', -8.0, 100.0)
(7, 'Name2', 50.0, 75.0, '10/15/2024', 8.0, 63.0)
(8, 'Name3', 200.0, 25.0, '10/15/2024', 8.0, 33.0)
```

### Add Rebalance hours column


Rebalance hours represents allows the Hours accrued to be gradually
introduced into the balance sheet with smoothing out would otherwize
would be a significant increase in the liabilities on the balance
sheet.

There are currently two versions, `rebalance_hours_raw.py` and `rebalance_hours.py`.
The `rebalance_hours_raw.py` version handles input from Katrinas
csv files and the `rebalance_hours.py` version handles the simple test
csv files I created, vacation_hours_*.csv. They both operate the
have the same parameters and usage but `rebalance_hours_raw.py`
needs to do more work because it in Katrina's csv files the there
is no UniqueId column and instead a ROWID column is added dynamically
to the table.

Here we remove all databases then load vactiona_hours_simple.csv then run rebalance_hours.py:
```
$ rm *.db; ./load.py vacation_hours.db vacation_hours_simple.csv vacation_hours && ./rebalance_hours.py vacation_hours
Data from 'vacation_hours_simple.csv' loaded into 'vacation_hours.db' as table 'vacation_hours'.
New records loaded: 3
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours, Rebalance_hours
----------------------------------------
(101, 'Name5', 80, 50, '2024-11-01', 8, 40, 8.0)
(104, 'Name4', 40, 25, '2024-11-01', 8, 8, 8.0)
(105, 'Name5', 80, 50, '2024-12-01', 8, 48, 16.0)
----------------------------------------
Total rows: 3
Rebalance hours updated for table 'vacation_hours'.
```

Next we load vacation_hours.csv and we see that all the Rebalance hours for
them is zero so they'll be processed when we next run rebalance_hours.py:
```
$ ./load.py vacation_hours
Data from 'vacation_hours.csv' loaded into 'vacation_hours.db' as table 'vacation_hours'.
New records loaded: 8
$ ./dump.py vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours, Rebalance_hours
----------------------------------------
(101, 'Name5', 80, 50, '2024-11-01', 8, 40, 8.0)
(104, 'Name4', 40, 25, '2024-11-01', 8, 8, 8.0)
(105, 'Name5', 80, 50, '2024-12-01', 8, 48, 16.0)
(1, 'Name1', 100, 50, '10/1/2024', 8, 102, 0.0)
(2, 'Name1', 100, 50, '10/1/2024', -2, 100, 0.0)
(3, 'Name2', 50, 75, '10/1/2024', 5, 55, 0.0)
(4, 'Name3', 200, 25, '10/1/2024', 8, 25, 0.0)
(5, 'Name1', 100, 50, '10/15/2024', 8, 108, 0.0)
(6, 'Name1', 100, 50, '10/15/2024', -8, 100, 0.0)
(7, 'Name2', 50, 75, '10/15/2024', 8, 63, 0.0)
(8, 'Name3', 200, 25, '10/15/2024', 8, 33, 0.0)
```

Now run rebalance_hours.py to update the new records Rebalance hours column
```
wink@3900x 24-11-23T22:50:24.501Z:~/prgs/katrina/vacation-hours-python (main)
$ ./rebalance_hours.py vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours, Rebalance_hours
----------------------------------------
(101, 'Name5', 80, 50, '2024-11-01', 8, 40, 8.0)
(104, 'Name4', 40, 25, '2024-11-01', 8, 8, 8.0)
(105, 'Name5', 80, 50, '2024-12-01', 8, 48, 16.0)
(1, 'Name1', 100, 50, '10/1/2024', 8, 102, 8.0)
(2, 'Name1', 100, 50, '10/1/2024', -2, 100, 8.0)
(3, 'Name2', 50, 75, '10/1/2024', 5, 55, 5.0)
(4, 'Name3', 200, 25, '10/1/2024', 8, 25, 8.0)
(5, 'Name1', 100, 50, '10/15/2024', 8, 108, 16.0)
(6, 'Name1', 100, 50, '10/15/2024', -8, 100, 16.0)
(7, 'Name2', 50, 75, '10/15/2024', 8, 63, 13.0)
(8, 'Name3', 200, 25, '10/15/2024', 8, 33, 16.0)
----------------------------------------
Total rows: 11
Rebalance hours updated for table 'vacation_hours'.
```

And we verify that the database table vacation_hours has been updated:
```
$ ./dump.py vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours, Rebalance_hours
----------------------------------------
(101, 'Name5', 80, 50, '2024-11-01', 8, 40, 8.0)
(104, 'Name4', 40, 25, '2024-11-01', 8, 8, 8.0)
(105, 'Name5', 80, 50, '2024-12-01', 8, 48, 16.0)
(1, 'Name1', 100, 50, '10/1/2024', 8, 102, 8.0)
(2, 'Name1', 100, 50, '10/1/2024', -2, 100, 8.0)
(3, 'Name2', 50, 75, '10/1/2024', 5, 55, 5.0)
(4, 'Name3', 200, 25, '10/1/2024', 8, 25, 8.0)
(5, 'Name1', 100, 50, '10/15/2024', 8, 108, 16.0)
(6, 'Name1', 100, 50, '10/15/2024', -8, 100, 16.0)
(7, 'Name2', 50, 75, '10/15/2024', 8, 63, 13.0)
(8, 'Name3', 200, 25, '10/15/2024', 8, 33, 16.0)
```

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.
