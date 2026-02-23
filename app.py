from flask import Flask, render_template,request,redirect,session
from datetime import date
import sqlite3
import pickle
import json

app=Flask(__name__)
app.secret_key="secret123"

DB="expenses.db"


model=pickle.load(open("model.pkl","rb"))
vectorizer=pickle.load(open("vectorizer.pkl","rb"))


def init_db():
    conn = sqlite3.connect(DB, check_same_thread=False)
    cur=conn.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password TEXT,daily_limit INTEGER)""")
    cur.execute(""" CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,amount INTEGER,reason TEXT,Category TEXT,date TEXT ,FOREIGN KEY (user_id) REFERENCES users(id))""")

    conn.commit()
    conn.close()

init_db()


@app.route("/",methods=["GET","POST"])
def login():
    error=None
    if request.method=="POST":
        username=request.form["username"].strip()
        password=request.form["password"].strip()
        daily_limit=request.form["daily_limit"].strip()
        

        conn = sqlite3.connect(DB, check_same_thread=False)
        cur=conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=? AND password=?",(username,password))
        user=cur.fetchone()
        conn.close()
        if user:
            if not daily_limit.isdigit():
                error="Daily limit must be a number"
            else:
                session["user_id"]=user[0]
                session["daily_limit"]=int(daily_limit)
            return redirect("/dashboard")
        else:
            error ="Invalid username or password"

    return render_template("login.html",error=error)


@app.route("/register",methods=["GET","POST"])
def register():
    error=None
    if request.method=="POST":
        username=request.form["username"].strip()
        password=request.form["password"].strip()
        daily_limit=request.form["daily_limit"].strip()
        if not daily_limit.isdigit():
            error="Daily limit must be a number"
        else:
            try:
                conn = sqlite3.connect(DB, check_same_thread=False)
                cur=conn.cursor()
                cur.execute("INSERT INTO users (username,password,daily_limit)VALUES(?,?,?)",(username,password,daily_limit))
           
                conn.commit()
                conn.close()
            
                return redirect("/")
            except sqlite3.IntegrityError:
                error="User already exists"
        

    return render_template("register.html",error=error)



@app.route("/dashboard")
def dashboard():
    if "user_id"not in session:
        return redirect("/")
    
    user_id =session["user_id"]
    daily_limit=session.get("daily_limit")
    conn = sqlite3.connect(DB, check_same_thread=False)
    cur=conn.cursor()

    cur.execute("SELECT amount,reason,Category,date FROM expenses WHERE user_id=?",(session["user_id"],))
    expenses=cur.fetchall()

    cur.execute("SELECT IFNULL(SUM(amount),0)FROM expenses WHERE user_id=?",(session["user_id"],))

    total=cur.fetchone()[0]

    cur.execute("SELECT daily_limit FROM users WHERE id=?",(session["user_id"],))

    limit=cur.fetchone()[0]

    cur.execute("""SELECT Category,SUM(amount) FROM expenses WHERE user_id=? GROUP BY Category """,(session["user_id"],))
    Chart_data=cur.fetchall()
    
    conn.close()

    labels=[row[0] for row in Chart_data]
    values=[row[1] for row in Chart_data]

    exceeded=total>limit

    
    summary = Chart_data  
    warning = "Daily limit exceeded!" if exceeded else ""

    

    return render_template("dashboard.html",expenses=expenses,total=total,limit=daily_limit,exceeded=exceeded,labels=labels,values=values,summary=summary,warning=warning)

@app.route("/add_expense",methods=["POST"])
def add_expense():
    if "user_id"not in session:
        return redirect("/")
    
    amount=request.form["amount"]
    reason=request.form["reason"]

    if reason.strip()=="":
        Category="Other"
    else:
        X=vectorizer.transform([reason])
        probs=model.predict_proba(X)[0]
        max_prob=max(probs)

        if max_prob<0.6:
            Category="Other"
        else:
            Category=model.predict(X)[0]
    

    today=date.today().isoformat()
    
    conn = sqlite3.connect(DB, check_same_thread=False)
    cur=conn.cursor()


    cur.execute("""INSERT INTO expenses (user_id,amount,reason,Category,date)VALUES(?,?,?,?,?)""",(session["user_id"],amount,reason,Category,today))
    
    conn.commit()
    conn.close()
        
    return redirect("/dashboard")





@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__=="__main__":
    app.run()
