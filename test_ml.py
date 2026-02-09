import pickle

model =pickle.load(open("model.pkl","rb"))
vectorizer=pickle.load(open("vectorizer.pkl","rb"))

text=["bus ticket"]
X=vectorizer.transform(text)
print(model.predict(X))