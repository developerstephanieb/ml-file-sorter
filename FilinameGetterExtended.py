#script for scraping filenames from Internet Archive
import internetarchive as ia 


def get_filenames(collection, num_file_names = 2000, file_types=None):
    if file_types is None:
        file_types = ['pdf', 'epub', 'txt', 'mp4', 'mp3', 'zip',  'mobi', 'djvu','exe']

    search = ia.search_items(
        f'collection:{collection}',
        fields=['identifier', 'title', 'date', 'mediatype']
    )

    print(f"Searching:{collection}")

    documents = []
    for i, item_data in enumerate(search):
        if i >= num_file_names:
            break

        item = ia.get_item(item_data['identifier'])
        files = item.get_files()

        for i, item_data in enumerate(search):
            if i >= num_file_names:
                break
            
            item = ia.get_item(item_data['identifier'])
            main_files = []


        selected_file = None
        for file in item.files:
            ext = file.name.split('.')[-1].lower()
            if ext in file_types and not file.name.endswith('_meta.xml'):
                selected_file = {
                    'name': file.name,
                    'size': f"{file.size:,} bytes" if file.size else "Unknown size",
                    'format': ext.upper()
                }
                break
        if selected_file != None:  # Only include items that have a relevant file
            documents.append({
                'id': item_data['identifier'],
                'title': item_data.get('title', 'No title'),
                'date': item_data.get('date', 'Unknown'),
                'mediatype': item_data.get('mediatype', 'Unknown'),
                'main_file': selected_file  # Single file instead of list
            })
        