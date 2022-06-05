import os
import csv
import time
import get_windows as x
import afk as y
from time_operations import time_difference

# get current time whenever the function is called
def get_time():
    t = os.popen('''date +"%T"''').read()
    return t[0:-1]

# get date of today
def get_date():
    d = os.popen('''date +"%Y-%m-%d"''').read()
    return d[0:-1]

def append_line_in_csv(date, closed_time, window_name):
    user = os.getlogin()
    filename = "/home/"+user+"/.cache/Watcher/raw_data/"+date+".csv"
    with open(filename, 'r') as file:
        last_app_time = file.readlines()[-1][0:8]

    time_spent = time_difference(last_app_time, closed_time)

    Data = [closed_time, time_spent,  window_name]
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t')
        csvwriter.writerow(Data)

# Expected Behaviour == if date got changed then append line in new csv file after initializing the csv file
# also if usr is AFK then append line

# TODO: AFK feature devlopement (it will be developed after completing alpha product (after whole project up end running)

def log_creation():
    filename = "/home/"+os.getlogin()+"/.cache/Watcher/raw_data/"+get_date()+".csv"
    if not(os.path.isfile(filename)):
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='\t')
            csvwriter.writerow([get_time(), "00:00:00", ""])
    append_line_in_csv(get_date(), get_time(), "User-logged-in")

    afk = False
    afkTimeout = 5 # timeout in minutes

    while True:
        previous_window = x.active_window()

        if (y.returned_from_afk(afk, afkTimeout)):
            previous_window = "AFK"
            afk = False

        if (x.is_window_changed(previous_window, afk, afkTimeout) and not afk):
            if(y.is_afk(afkTimeout)):
                afk = True
            closed_at = get_time() # for next_window its the opening time
            date = get_date()
            filename = "/home/"+os.getlogin()+"/.cache/Watcher/raw_data/"+date+".csv"
            if not(os.path.isfile(filename)):
                with open(filename, 'a') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter='\t')
                    prev_date = os.popen("""date -d "yesterday" '+%Y-%m-%d'""").read()[0:-1]
                    prev_file = "/home/"+os.getlogin()+"/.cache/Watcher/raw_data/"+prev_date+".csv"
                    with open(prev_file, 'r') as file:
                        last_app_time = file.readlines()[-1][0:8]
                    csvwriter.writerow([get_time(), time_difference(last_app_time, closed_at), (os.popen('/usr/share/Watcher/afk').read())])

            else:
                # appends line when app gets closed
                append_line_in_csv(date, closed_at, previous_window)
       
if __name__ == "__main__":
    log_creation()
