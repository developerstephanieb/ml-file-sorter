#script for scraping filenames from Internet Archive

from sklearn.datasets import fetch_20newsgroups


categories = ['rec.autos', 'sci.space', 'comp.graphics', 'talk.religion.misc']
print("Fetching 20 newsgroups dataset with categories:", categories)
data = fetch_20newsgroups(subset='all', categories=categories)
print(len(data.data))        
print(data.target_names)    
print(data.filenames[:5])  
