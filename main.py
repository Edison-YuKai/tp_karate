from time import sleep
import numpy as np
import inquirer
import csv
import datetime
from inquirer import errors
from os import name, system

def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 

    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def load_csv_data(filename) -> list:
    # Function to load CSV data from the given file name and return it as a li5st of lists.
    openfile = open(filename)  # Open the file with the given file name.
    csvreader = csv.reader(openfile)  # Create a CSV reader object to read the file.
    datalist = [row for row in csvreader]  # Initialize an empty list to store the data.

    return np.array(datalist)  # Return the final list of lists containing the CSV data.

members_array = load_csv_data("members.csv")
venues_array = load_csv_data("venues.csv")

members_array = np.c_[members_array, np.zeros(members_array.shape[0])] 
members_array[0,-1] = "Attendance"

venue = inquirer.list_input("Select venue",
                choices=[venue[0] for venue in venues_array[1:]],
                carousel=True,)

def validate_day(answers, current):
    try:
        if int(current)<=0 or int(current)>=32:
            raise errors.ValidationError('', reason='Invalid day.')
        return True
    except ValueError:
        raise errors.ValidationError('', reason='Only numbers allowed.')
def validate_year(answers, current):
    try:
        if int(current)<=2022:
            raise errors.ValidationError('', reason='Invalid year, only 2023 and above.')
        return True
    except ValueError:
        raise errors.ValidationError('', reason='Only numbers allowed.')

while True:
    year = inquirer.text(message="Year", validate=validate_year)
    month = inquirer.list_input("Select month",
                    choices=[('January',1 ), ('February',2), ('March',3), ('April',4), ('May',5), ('June',6), ('July',7), ('August',8) , ('September',9), ('October',10), ('November',11), ('December',12)],
                    carousel=True,)
    day = inquirer.text(message="Day", validate=validate_day)
    try:
        datetime.datetime(year=int(year),month=int(month),day=int(day))
        date = str(day) + '/' + str(month) + '/' + str(year)
        break
    except ValueError:
        print("Invalid date given")

output = []
output.extend([["Venue", venue],[],["Date", date],[]])

students_attended = []

while True:
    clear()
    print(students_attended)
    print('''
Select which members attended this lesson

1 -> Unselect last member
2 -> Confirm selection
Any other input -> Search for members by their name
          ''')
    search_term = inquirer.text(message="Input")
    matching_results = [member for member in members_array[1:] if search_term.lower() in member[0].lower()]

    if search_term == "2":
        break
    if search_term == "1" and len(students_attended)>0:
            del students_attended[-1]
    # Display matching results and allow user to select attendees
    attendee_choices = [(f"{i + 1}. {result[0]}", result[0]) for i, result in enumerate(matching_results)]
    if attendee_choices != []:
        selection = inquirer.list_input("Select attendee", choices=attendee_choices)
        if selection not in students_attended:
            students_attended.append(selection)

for student in students_attended:
    print(np.where(members_array == student))
    members_array[np.where(members_array == student)[0],4]=1

for row in members_array:
    output.append(row.tolist())

print(output)
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output)