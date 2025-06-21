# ML File Sorter

This project implements a basic machine learning-based file sorter. It scans a directory for files and automatically moves each file into an appropriate folder based on its filename. The classifier learns from labeled examples and can generalize to new, unseen filenames.

## How It Works

1. Training the Model
- The model is trained on a CSV file (data/labeled_files.csv) containing filenames and their corresponding categories (folder names).
- It uses a TF-IDF Vectorizer to extract features from the file names.
- A Multinomial Naive Bayes classifier is trained to predict the folder/category for a given filename.

2. File Sorting
- The trained model is loaded from disk (model/classifier.pkl).
- Files placed in the data/files_to_sort/directory are passed to the model.
- Based on the predicted category, each file is moved to a subfolder within the folders/ directory.

3. Example Folders
Supported categories (and folders) include:
- Work
- School
- Pictures

If a predicted category does not exist, it will be created automatically.

### Machine Learning Implementation

This project uses supervised learning, where a model is trained on labeled examples of file names and their corresponding folder categories. The model learns to map input text (file names) to output labels (folders) based on patterns found in the training data.

## Project Structure
```
ml_file_sorter/
├── data/
│   ├── labeled_files.csv        # Labeled training data
│   └── files_to_sort/           # Files to be classified
├── folders/                     # Destination folders for sorted files
│   ├── Work/
│   ├── School/
│   └── Pictures/
├── model/
│   └── classifier.pkl           # Trained classifier
├── train.py                     # Script to train and save the model
└── sorter.py                    # Script to sort files using the model
```

## Usage
Step 1: Install Requirements
```
pip3 install scikit-learn pandas joblib
```
Step 2: Train the Model
```
python3 train.py
```
Step 3: Sort Files.  
Place files in data/files_to_sort/, then run:
```
python3 sorter.py
```
Files will be moved into folders/<predicted_category>/.

## Improvements
- Add support for file extension and metadata features
- Include user feedback to refine predictions (semi-supervised learning)