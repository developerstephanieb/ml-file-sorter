import os
import csv

# Define your parameters here 
scan_folder = r"folders\School"  # or just "folders/Pictures" for cross-platform
mark_files_as = "School"  # Category to mark files as
save_path = r"data\labeled_files.csv"

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to scan
    scan_path = os.path.join(script_dir, scan_folder)
    scan_path = os.path.normpath(scan_path)
    
    print(f"Script directory: {script_dir}")
    print(f"Scanning directory: {scan_path}")
    
    # Check if the directory exists
    if not os.path.exists(scan_path):
        print(f"Error: Directory '{scan_path}' does not exist!")
        print("Available directories:")
        try:
            folders_path = os.path.join(script_dir, "folders")
            if os.path.exists(folders_path):
                for item in os.listdir(folders_path):
                    item_path = os.path.join(folders_path, item)
                    if os.path.isdir(item_path):
                        print(f"  - folders/{item}")
            else:
                print("  'folders' directory not found!")
        except Exception as e:
            print(f"  Error listing directories: {e}")
        return
    
    # Get all FILES in the scan path (CHANGED FROM DIRECTORIES)
    try:
        print("Scanning for files under:", scan_path)
        file_names = []  # Changed variable name
        for item in os.listdir(scan_path):
            item_path = os.path.join(scan_path, item)
            if os.path.isfile(item_path):  # Changed from os.path.isdir() to os.path.isfile()
                file_names.append(item)  # Changed variable name
        
        print(f"Found {len(file_names)}")  # Updated message
        
    except Exception as e:
        print(f"Error scanning directory: {e}")
        return
    
    if not file_names:  # Changed variable name
        print("No files found in the specified scan path.")  # Updated message
        return
    
    # Path to the CSV file
    csv_path = os.path.join(script_dir, save_path)
    
    # Create the data directory if it doesn't exist
    csv_dir = os.path.dirname(csv_path)
    if not os.path.exists(csv_dir):
        print(f"Creating directory: {csv_dir}")
        os.makedirs(csv_dir)
    
    # Create CSV file with header if it doesn't exist
    if not os.path.exists(csv_path):
        print(f"Creating new CSV file: {csv_path}")
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['file_name', 'category'])  # write header row
        except Exception as e:
            print(f"Error creating CSV file: {e}")
            return
    
    # Read existing data from CSV
    existing_data = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)  # skip header row safely
            for row in csvreader:
                if len(row) >= 2:  # ensure row has at least 2 columns
                    existing_data[row[0]] = row[1]
        
        print(f"Found {len(existing_data)} existing entries in CSV")
        
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Add new data to CSV
    new_entries = 0
    skipped_entries = 0
    try:
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            for file_name in file_names:  # Changed variable name
                if file_name not in existing_data:
                    csvwriter.writerow([file_name, mark_files_as])
                    new_entries += 1
                    print(f"Added: {file_name} -> {mark_files_as}")
                else:
                    skipped_entries += 1
                
        print(f"\nCompleted! Added {new_entries} new entries to {csv_path} and skipped {skipped_entries} existing entries.")
        
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    main()