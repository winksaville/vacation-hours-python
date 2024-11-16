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

Seems to be working!

Here we remove all databased then load vactiona_hours_simple.csv then run p1_exper.py:
```
wink@3900x 24-11-16T21:24:11.931Z:~/prgs/katrina/vacation-hours-python (v0.2.0-wip)
$ rm *.db; ./load.py vacation_hours.db vacation_hours_simple.csv vacation_hours && ./p1_exper.py vacation_hours
Data from 'vacation_hours_simple.csv' loaded into 'vacation_hours.db' as table 'vacation_hours'.
New records loaded: 3
DEBUG: Added 'Rebalance_hours' column to vacation_hours
DEBUG: update_reblance_hours:+
DEBUG: update_reblance_hours: TOL row: ('104', 'Name4', '40', '25', '2024-11-01', '8', '8', 0)
DEBUG: update_reblance_hours: new name: Name4 previous_name: None
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 8
DEBUG: update_reblance_hours: rebalance_hours: 8
DEBUG: update_reblance_hours: BOL rebalance_hours: 8 previous_rebalance_hours: 8 previous_name: Name4
DEBUG: update_reblance_hours: TOL row: ('101', 'Name5', '80', '50', '2024-11-01', '8', '40', 0)
DEBUG: update_reblance_hours: new name: Name5 previous_name: Name4
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 8
DEBUG: update_reblance_hours: rebalance_hours: 8
DEBUG: update_reblance_hours: BOL rebalance_hours: 8 previous_rebalance_hours: 8 previous_name: Name5
DEBUG: update_reblance_hours: TOL row: ('105', 'Name5', '80', '50', '2024-12-01', '8', '48', 0)
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 8
DEBUG: update_reblance_hours: rebalance_hours: 16
DEBUG: update_reblance_hours: BOL rebalance_hours: 16 previous_rebalance_hours: 16 previous_name: Name5
DEBUG: update_reblance_hours:-
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours, Rebalance_hours
----------------------------------------
('101', 'Name5', '80', '50', '2024-11-01', '8', '40', 8)
('104', 'Name4', '40', '25', '2024-11-01', '8', '8', 8)
('105', 'Name5', '80', '50', '2024-12-01', '8', '48', 16)
----------------------------------------
Total rows: 3
Rebalance hours updated for table 'vacation_hours'.
wink@3900x 24-11-16T21:24:18.493Z:~/prgs/katrina/vacation-hours-python (v0.2.0-wip)
```

Next we load vacation_hours.csv and we see that all the Rebalance hours for
them is zero so they'll be processed when we next run p1_exper.py:
```
wink@3900x 24-11-16T21:24:18.493Z:~/prgs/katrina/vacation-hours-python (v0.2.0-wip)
$ ./load.py vacation_hours
Data from 'vacation_hours.csv' loaded into 'vacation_hours.db' as table 'vacation_hours'.
New records loaded: 8
wink@3900x 24-11-16T21:24:36.818Z:~/prgs/katrina/vacation-hours-python (v0.2.0-wip)
$ ./dump.py vacation_hours
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours, Rebalance_hours
----------------------------------------
('101', 'Name5', '80', '50', '2024-11-01', '8', '40', 8)
('104', 'Name4', '40', '25', '2024-11-01', '8', '8', 8)
('105', 'Name5', '80', '50', '2024-12-01', '8', '48', 16)
('1', 'Name1', '100', '50', '2024-10-01', '8', '102', 0)
('2', 'Name1', '100', '50', '2024-10-01', '-2', '100', 0)
('3', 'Name2', '50', '75', '2024-10-01', '5', '55', 0)
('4', 'Name3', '200', '25', '2024-10-01', '8', '25', 0)
('5', 'Name1', '100', '50', '2024-10-15', '8', '108', 0)
('6', 'Name1', '100', '50', '2024-10-15', '-8', '100', 0)
('7', 'Name2', '50', '75', '2024-10-15', '8', '63', 0)
('8', 'Name3', '200', '25', '2024-10-15', '8', '33', 0)
wink@3900x 24-11-16T21:24:45.190Z:~/prgs/katrina/vacation-hours-python (v0.2.0-wip)
```

Now run p1_exper.py and
```
wink@3900x 24-11-16T21:24:45.190Z:~/prgs/katrina/vacation-hours-python (v0.2.0-wip)
$ ./p1_exper.py vacation_hours
DEBUG: update_reblance_hours:+
DEBUG: update_reblance_hours: TOL row: ('1', 'Name1', '100', '50', '2024-10-01', '8', '102', 0)
DEBUG: update_reblance_hours: new name: Name1 previous_name: None
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 8
DEBUG: update_reblance_hours: rebalance_hours: 8
DEBUG: update_reblance_hours: BOL rebalance_hours: 8 previous_rebalance_hours: 8 previous_name: Name1
DEBUG: update_reblance_hours: TOL row: ('2', 'Name1', '100', '50', '2024-10-01', '-2', '100', 0)
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: set rebalance_hours: 0 to 8
DEBUG: update_reblance_hours: rebalance_hours: 8
DEBUG: update_reblance_hours: BOL rebalance_hours: 8 previous_rebalance_hours: 8 previous_name: Name1
DEBUG: update_reblance_hours: TOL row: ('5', 'Name1', '100', '50', '2024-10-15', '8', '108', 0)
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 8
DEBUG: update_reblance_hours: rebalance_hours: 16
DEBUG: update_reblance_hours: BOL rebalance_hours: 16 previous_rebalance_hours: 16 previous_name: Name1
DEBUG: update_reblance_hours: TOL row: ('6', 'Name1', '100', '50', '2024-10-15', '-8', '100', 0)
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: set rebalance_hours: 0 to 16
DEBUG: update_reblance_hours: rebalance_hours: 16
DEBUG: update_reblance_hours: BOL rebalance_hours: 16 previous_rebalance_hours: 16 previous_name: Name1
DEBUG: update_reblance_hours: TOL row: ('3', 'Name2', '50', '75', '2024-10-01', '5', '55', 0)
DEBUG: update_reblance_hours: new name: Name2 previous_name: Name1
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 5
DEBUG: update_reblance_hours: rebalance_hours: 5
DEBUG: update_reblance_hours: BOL rebalance_hours: 5 previous_rebalance_hours: 5 previous_name: Name2
DEBUG: update_reblance_hours: TOL row: ('7', 'Name2', '50', '75', '2024-10-15', '8', '63', 0)
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 8
DEBUG: update_reblance_hours: rebalance_hours: 13
DEBUG: update_reblance_hours: BOL rebalance_hours: 13 previous_rebalance_hours: 13 previous_name: Name2
DEBUG: update_reblance_hours: TOL row: ('4', 'Name3', '200', '25', '2024-10-01', '8', '25', 0)
DEBUG: update_reblance_hours: new name: Name3 previous_name: Name2
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 8
DEBUG: update_reblance_hours: rebalance_hours: 8
DEBUG: update_reblance_hours: BOL rebalance_hours: 8 previous_rebalance_hours: 8 previous_name: Name3
DEBUG: update_reblance_hours: TOL row: ('8', 'Name3', '200', '25', '2024-10-15', '8', '33', 0)
DEBUG: update_reblance_hours: rebalance_hours: 0 == 0
DEBUG: update_reblance_hours: inc rebalance_hours: 0 by  hours_accrued: 8
DEBUG: update_reblance_hours: rebalance_hours: 16
DEBUG: update_reblance_hours: BOL rebalance_hours: 16 previous_rebalance_hours: 16 previous_name: Name3
DEBUG: update_reblance_hours: TOL row: ('104', 'Name4', '40', '25', '2024-11-01', '8', '8', 8)
DEBUG: update_reblance_hours: new name: Name4 previous_name: Name3
DEBUG: update_reblance_hours: rebalance_hours: 8 != 0,  ignore because we've updated in a previous run!
DEBUG: update_reblance_hours: BOL rebalance_hours: 8 previous_rebalance_hours: 8 previous_name: Name4
DEBUG: update_reblance_hours: TOL row: ('101', 'Name5', '80', '50', '2024-11-01', '8', '40', 8)
DEBUG: update_reblance_hours: new name: Name5 previous_name: Name4
DEBUG: update_reblance_hours: rebalance_hours: 8 != 0,  ignore because we've updated in a previous run!
DEBUG: update_reblance_hours: BOL rebalance_hours: 8 previous_rebalance_hours: 8 previous_name: Name5
DEBUG: update_reblance_hours: TOL row: ('105', 'Name5', '80', '50', '2024-12-01', '8', '48', 16)
DEBUG: update_reblance_hours: rebalance_hours: 16 != 0,  ignore because we've updated in a previous run!
DEBUG: update_reblance_hours: BOL rebalance_hours: 16 previous_rebalance_hours: 16 previous_name: Name5
DEBUG: update_reblance_hours:-
Table: vacation_hours
Columns: UniqueId, Name, Max_vacation_hours, Hourly_wage, Transaction_date, Hours_accrued, Balance_hours, Rebalance_hours
----------------------------------------
('101', 'Name5', '80', '50', '2024-11-01', '8', '40', 8)
('104', 'Name4', '40', '25', '2024-11-01', '8', '8', 8)
('105', 'Name5', '80', '50', '2024-12-01', '8', '48', 16)
('1', 'Name1', '100', '50', '2024-10-01', '8', '102', 8)
('2', 'Name1', '100', '50', '2024-10-01', '-2', '100', 8)
('3', 'Name2', '50', '75', '2024-10-01', '5', '55', 5)
('4', 'Name3', '200', '25', '2024-10-01', '8', '25', 8)
('5', 'Name1', '100', '50', '2024-10-15', '8', '108', 16)
('6', 'Name1', '100', '50', '2024-10-15', '-8', '100', 16)
('7', 'Name2', '50', '75', '2024-10-15', '8', '63', 13)
('8', 'Name3', '200', '25', '2024-10-15', '8', '33', 16)
----------------------------------------
Total rows: 11
Rebalance hours updated for table 'vacation_hours'.
wink@3900x 24-11-16T21:25:05.574Z:~/prgs/katrina/vacation-hours-python (v0.2.0-wip)
```

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.
