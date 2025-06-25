import os
import shutil
import joblib


if __name__ == "__main__":
    SOURCE_DIR = "data/files_to_sort"
    DEST_BASE_DIR = "folders"
    TRAIN_DIR = "data/ia_files.csv"

    training_list = set()

    if os.path.exists(TRAIN_DIR):
        with open(TRAIN_DIR, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    training_list.add(parts[0])

    model = joblib.load("model/classifier.pkl")

    for fname in os.listdir(SOURCE_DIR):
        if fname in training_list:
            print(f"Waring! '{fname}' is in the training set and should not be used for mesureing model accuracy.")
            
        if os.path.isfile(os.path.join(SOURCE_DIR, fname)):
            pred = model.predict([fname])[0]
            dest_dir = os.path.join(DEST_BASE_DIR, pred)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(os.path.join(SOURCE_DIR, fname),
                        os.path.join(dest_dir, fname))
            print(f"Moved '{fname}' to '{pred}'")

