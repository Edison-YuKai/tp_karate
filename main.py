import numpy as np
import inquirer
import csv
from datetime import datetime
from inquirer import errors
from os import name, system
import os

stats_string = "View attendance stats"
attendance_string = "Add new attendance sheet"

def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 

    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def load_csv_data(filename):
    openfile = open(filename)
    csvreader = csv.reader(openfile)
    datalist = [row for row in csvreader]
    return datalist

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

menu = inquirer.list_input("Select choice",
                choices=[(attendance_string,1), (stats_string, 2), ("Quit",3)],
                carousel=True,)

match(menu):
    case(1):
        print(f"Your selected {attendance_string}")
        members_array = np.array(load_csv_data("members.csv"))
        venues_array = np.array(load_csv_data("venues.csv"))

        members_array = np.c_[members_array, np.zeros(members_array.shape[0])] 
        members_array[0,-1] = "Attendance"

        venue = inquirer.list_input("Select venue",
                        choices=[venue[0] for venue in venues_array[1:]],
                        carousel=True,)

        while True:
            year = inquirer.text(message="Year", validate=validate_year, default=int(datetime.today().strftime('%Y')))
            month = inquirer.list_input("Select month",
                            choices=[('January',1 ), ('February',2), ('March',3), ('April',4), ('May',5), ('June',6), ('July',7), ('August',8) , ('September',9), ('October',10), ('November',11), ('December',12)],
                            carousel=True,
                            default=int(datetime.today().strftime('%m')))
            day = inquirer.text(message="Day", validate=validate_day, default=int(datetime.today().strftime('%d')))
            try:
                datetime(year=int(year),month=int(month),day=int(day))
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

        # Specify the directory path and file name
        directory = "attendance"
        filename = f'{day}-{month}-{year}.csv'  # Using a hyphen as separator

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create the CSV file
        filepath = os.path.join(directory, filename)

        for row in members_array:
            output.append(row.tolist())

        with open(filepath, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(output)
    case(2):
        print(f"You selected: {stats_string}")
        # Specify the directory path
        directory = "attendance"

        # List all files in the directory
        file_list = os.listdir(directory)

        # Filter only CSV files
        csv_files = [file for file in file_list if file.endswith('.csv')]

        big_list = []
        # Read and process each CSV file
        for csv_file in csv_files:
            filepath = os.path.join(directory, csv_file)
            big_list.append(load_csv_data(filepath))
        
        total_trainings_dict = {
                "Monday": 0,
                "Tuesday": 0,
                "Wednesday": 0,
                "Thursday": 0,
                "Friday": 0,
                "Saturday": 0,
                "Sunday": 0
        }
        members_attendance_dict = {}

        members_array = load_csv_data('members.csv')[1:]

        for member in members_array:
            members_attendance_dict[member[0]]={
                "Monday": 0,
                "Tuesday": 0,
                "Wednesday": 0,
                "Thursday": 0,
                "Friday": 0,
                "Saturday": 0,
                "Sunday": 0
            }


        for list in big_list:

            date_parts = list[2][1].split("/")  # Split the date string into day, month, and year parts
            day, month, year = int(date_parts[0]),int(date_parts[1]),int(date_parts[2])
            date = datetime(year=year, month=month, day=day)

            # Get the day of the week (0 = Monday, 6 = Sunday)
            day_of_week = date.weekday()
            
            # Define a list of day names
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            
            total_trainings_dict[days[day_of_week]] += 1
            
            for row in np.array(list[5:]):
                if row[-1]=='1':
                    members_attendance_dict[row[0]][days[day_of_week]] += 1

        output = [["Full Name", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday","Tues%","TuesThurs%", "All%"]]
        # Iterate through the outer dictionary
        for outer_key, inner_dict in members_attendance_dict.items():
            row = []
            row.append(outer_key)
            # Iterate through the inner dictionary
            for inner_key, inner_value in inner_dict.items():
                row.append(inner_value)
            row.append(row[2]/total_trainings_dict['Tuesday'])
            row.append((row[2] + row[4])/(total_trainings_dict['Tuesday']+total_trainings_dict['Thursday']))
            row.append((row[2] + row[4]+ row[6])/(total_trainings_dict['Tuesday']+total_trainings_dict['Thursday']+total_trainings_dict['Saturday']))
            output.append(row)
        print(0/1)
        # Specify the directory path and file name
        directory = "stats"
        filename = 'stats.csv'  # Using a hyphen as separator

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create the CSV file
        filepath = os.path.join(directory, filename)

        with open(filepath, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(output)
