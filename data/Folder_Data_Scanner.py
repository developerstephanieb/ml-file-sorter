# Folder_Data_Scanner
# This script scans data and then adds it to the labeld files.csv data 
# this will make it so we dont have to manually enter each folder name and category

# define your paramaters here 
THE_DIRECTORY_TO_SCAN = r"folders\School"
THEY_WILL_BE_MARKED_AS = "School"
THEY_WILL_BE_SAVED_AS = r"folders\School\files.csv"

import os
import csv

Scan_Directory,Category,Save_Path_csv = THE_DIRECTORY_TO_SCAN,THEY_WILL_BE_MARKED_AS,THEY_WILL_BE_SAVED_AS

File_Names = [f.name for f in os.scandir(Scan_Directory) if f.is_dir()]

if not os.path.exists(os.path.dirname(Save_Path_csv)):
    os.makedirs(os.path.dirname(Save_Path_csv))
    with open(Save_Path_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Name', 'Category'])
    
with open(Save_Path_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader) # skip header row
    existing_data = {rows[0]: rows[1] for rows in csvreader if rows}

with open(Save_Path_csv, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)    # add new data
    for file_name in File_Names:
        if file_name not in existing_data:
            csvwriter.writerow([file_name, Category])