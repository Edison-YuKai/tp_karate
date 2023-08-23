# TP Karate
MVP: a python program to help mark training attendance

1. this program will accept these CSV files:

- members.csv (csv file containing data on karate members)

- venues.csv (csv file containing the training venues)

2. create attendance sheets under /attendance

3. create stats sheet under /stats
    - attendance % for tuesdays
    - attendance % for tuesdays, thursdays
    - attendance % for tuesdays, thursdays, saturdays

## Areas for improvement

- error handling (making a stats file when there is no attendance sheets)
- stats sheet display %
- dynamic stats (dont display day fields with 0 trainings on them)
- generate a html file from display stats sheet and auto-open html file
- be able to generate stats for a custom period of time (1 term, 1 sem, trials period, etc.)

Current bug:
If you make statistics and some members did not attend certain days of training at all (example I skip every Tuesday training), the member's row will not put 0 on 'Tuesday' but instead shift everything left.

Issue is in line 170-199

Possible solutions:
- Create variables for which index is which day of training
- Make a numpy array?!!! *****
