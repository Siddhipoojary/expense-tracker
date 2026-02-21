from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

reason=[
    "tea coffee snacks ",
    "cafe ",
    "breakfast lunch dinner ",
    "pizza burger fries ",
    "street food panipuri",
    "cake icecream juice ",
    "canteen ",
    "bus train ticket flight ",
    "auto cab uber ola metro ",
    "parking toll ",
    "movie popcorn",
    " shopping",
    " netfix spotify amazon prime ",
    "gaming concert",
    "mobile reacharge internet wifi internet",
    " pg rent ",
    "vegetables groceries rice fruits ",
    "supermarket ",
    "electricity bill",
    "restaurant dinner",
    "petrol diesel fuel"
]

Categories=[
    "Food",
    "Food",
    "Food",
    "Food",
    "Food",
    "Food",
    "Food", 
    "Transport",
    "Transport",
    "Transport",
    "Entertainment",
    "Entertainment",
    "Entertainment",
    "Entertainment",
    "Utilities",
    "Utilities",
    "Groceries",
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
