from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

reason=[
    "tea coffee snacks",
    "bus train ticket",
    "movie popcorn",
    "mobile reacharge internet",
    "vegetables groceries rice",
    "electricity bill",
    "restaurant dinner",
    "petrol diesel fuel"
]

Categories=[
    "Food",
    "Transport",
    "Entertainment",
    "Utilities",
    "Groceries",
    "Utilities",
    "Food",
    "Transport"
]

vectorizer=CountVectorizer()
X=vectorizer.fit_transform(reason)

model=MultinomialNB()
model.fit(X, Categories)

pickle.dump(model,open("model.pkl","wb"))
pickle.dump(vectorizer,open("vectorizer.pkl","wb"))

print("ML model trained & saved")
