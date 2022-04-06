import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from joblib import dump, load
import pickle

dataset = pd.read_csv('CrawlsLabelled.csv') #You need to change #directory accordingly
print(dataset[['Parsed', 'Param']]) #Return 10 rows of data


z = dataset['URL']
y = dataset["Parsed"]
x = dataset['Param']
z_train, z_test, y_train, y_test, x_train, x_test = train_test_split(z, y, x, test_size = 0.2)

cv = CountVectorizer()
contentFeatures = cv.fit_transform(y_train)
print(contentFeatures)

#so we used y_train for the count vectorizor.
# now we will use the labels from x_train

model = svm.SVC()
model.fit(contentFeatures,x_train)

features_test = cv.transform(y_test)
print("Accuracy: {}".format(model.score(features_test,x_test)))

# Save the vectorizer
vec_file = 'contentVector.pickle'
pickle.dump(cv, open(vec_file, 'wb'))

# Save the model
mod_file = 'conteUsefulness.model'
pickle.dump(model, open(mod_file, 'wb'))