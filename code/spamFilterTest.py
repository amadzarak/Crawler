from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
import pickle

# https://www.bbc.com/news/world-us-canada-61005388
X_test = ["You are a poop"]

# load the vectorizer
loaded_vectorizer = pickle.load(open('contentVector.pickle', 'rb'))

    # load the model
loaded_model = pickle.load(open('conteUsefulness.model', 'rb'))

    # make a prediction
print(loaded_model.predict(loaded_vectorizer.transform(X_test)))