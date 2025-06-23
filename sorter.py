import os
import shutil
import joblib


if __name__ == "__main__":
    SOURCE_DIR = "data/files_to_sort"
    DEST_BASE_DIR = "folders"

    model = joblib.load("model/classifier.pkl")

    for fname in os.listdir(SOURCE_DIR):
        if os.path.isfile(os.path.join(SOURCE_DIR, fname)):
            pred = model.predict([fname])[0]
            dest_dir = os.path.join(DEST_BASE_DIR, pred)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(os.path.join(SOURCE_DIR, fname),
                        os.path.join(dest_dir, fname))
            print(f"Moved '{fname}' to '{pred}'")