# TP Karate
MVP: a python program to help mark training attendance

1. this program will accept these CSV files:

- members.csv (csv file containing data on karate members)
    - fields:
        - full name
        - seniority (trials, freshman, junior, senior)

- venues.csv (csv file containing the training venues)
    - fields:
        - venue name

2. read these files and then turn them into numpy arrays

3. prompt the user to:
    - select venue
    - input date (with input validation)

4. ask the user to continually select the members attending this current training.

    as the user types, the matching options will be displayed, of which the user can select (arrow keys to select, enter to confirm)

5. after user has selected all the members, output a csv file containing the fully furnished attendance list for that training in csv format