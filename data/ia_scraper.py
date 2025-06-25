# Script for scraping filenames from Internet Archive

# Script for scraping filenames from Internet Archive
import internetarchive as ia 
import os
import csv
import time

def get_filenames(collection, num_file_names=2000, save_dir=r'data\ia_files.csv'):

    TEST_FILE_DIR = r'data\test_files'
    Test_file_Names = set()
    if os.path.exists(TEST_FILE_DIR):
        for dirpath,dirnames, filenames in os.walk(TEST_FILE_DIR):
            for filename in filenames:
                Test_file_Names.add(filename.lower())
    else:
        print(f"WARNING!!!:Test file directory '{TEST_FILE_DIR}' does not exist, skipping test file check.")


    search = ia.search_items(
        f'collection:{collection}',
        fields=['identifier', 'title', 'date', 'mediatype']
    )

    
    print(f"Searching: {collection}....this may take some time")
    
    search_list = list(search)
    print(f"Search complete found {len(search_list)} total items in collection")
    
    if len(search_list) == 0:
        print(f"ERROR No items found for collection '{collection}'")
        return []

    found_files = []
    processed_count = 0
    
    for i, item_data in enumerate(search_list):
        if i >= num_file_names:
            break
            
        processed_count += 1
        print(f"Processing item {i}: {item_data.get('identifier', 'Unknown ID')}")

        item = ia.get_item(item_data['identifier'])
        time.sleep(0.1) #prevent rate limiting issues
        
        selected_file = None
        file_count = 0
        #skip metadata files and thumbnails
        skip_keywords = ['_meta.xml', '_files.xml', '_thumb', '.xml', '.json', '.m3u', '.png', '.jpg', '.jpeg'] 
        
        for file in item.files:
            name = file.get('name', '').lower()
            if any(skip in name for skip in skip_keywords):
                continue
            
            # Check file size to skip tiny files
            if file.get('size') and int(file['size']) < 1000:
                continue
                
            selected_file = {
                'name': file['name'],
                'format': file['name'].split('.')[-1].lower() if '.' in file['name'] else 'UNKNOWN'
            }
            print(f"Selected file: {file['name']}")
            file_count += 1
            break
        
        if file_count == 0:
            print(f"No files found for item {item_data.get('identifier')} : {collection} skipping ")
        elif selected_file is None:
            print(f"No matching file types found in {file_count} files for item {item_data.get('identifier')} : {collection}")
        
        if selected_file is not None and selected_file['name'].lower() not in Test_file_Names: 
            found_files.append({
                'id': item_data['identifier'],
                'title': item_data.get('title', 'No title'),
                'mediatype': item_data.get('mediatype', 'Unknown'),
                'main_file': selected_file 
            })
        
        # Save progress every 100 processed items
        if processed_count % 100 == 0:
            print(f"Processed {processed_count} items so far, found {len(found_files)} valid files")
            if found_files:  # Only save if we have files to save
                save_progress(found_files, collection, save_dir=save_dir)
                found_files = []  # Reset after saving
        
        if processed_count % 10 == 0: 
            print(f"Retrieved {processed_count} documents, found {len(found_files)} with matching files in current batch")
    
    if found_files:
        save_progress(found_files, collection, save_dir=save_dir)
    

def initialize_csv(save_dir):
    if not os.path.exists(save_dir):
        with open(save_dir, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['file_name', 'category'])  # Header row
            print(f"Created new CSV file: {save_dir}")
    else:
        print(f"Using existing CSV file: {save_dir}")

def save_progress(files, collection_name, save_dir=r'data\ia_files.csv'):
    # Read existing data

    initialize_csv(save_dir)
    print(f"Saving progress for category: {collection_name} to {save_dir}")

    existing_data = set() # more efficient than list or dict
    try:
        with open(save_dir, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)  # Skip header
            for row in csvreader:
                if len(row) >= 1: 
                    existing_data.add(row[0])  # Add filename to set
        
        print(f"Found {len(existing_data)} existing entries in CSV")
    except FileNotFoundError:
        print("CSV file not found")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Prepare new entries
    new_entries = 0
    skipped_entries = 0
    
    try:
        with open(save_dir, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            for file_data in files:
                if 'main_file' in file_data and 'name' in file_data['main_file']:
                    file_name = file_data['main_file']['name']
                    
                    if file_name not in existing_data:
                        csvwriter.writerow([file_name, collection_name])
                        existing_data.add(file_name)  # Add to set to avoid duplicates in this batch
                        new_entries += 1
                        print(f"Added: {file_name} -> {collection_name}")
                    else:
                        skipped_entries += 1
                        
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return
                
    print(f"Batch complete! Added {new_entries} new entries, skipped {skipped_entries} duplicates.")


if __name__ == "__main__":
    save_dir = r'data\ia_files.csv'
    
    initialize_csv(save_dir)
    
    collection_targets = [
        #'gutenberg',
        "folkscanomy", 
        "softwarelibrary_msdos", 
        "prelinger",
    ]
        
    for collection in collection_targets:
        print('-' * 50)
        print(f"Processing collection: {collection}")

        files = get_filenames(collection, num_file_names=4000, save_dir=save_dir)  # Reduced for testing
        if not files:
            print(f"No files found for collection: {collection}")
            continue
        print(f"Finished processing collection: {collection}")
        print(f"Found {len(files)} files total")
        print()