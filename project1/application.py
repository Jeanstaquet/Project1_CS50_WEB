import os
import json
from flask import Flask, session, render_template, request, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('home.html')

@app.route("/loggin", methods=["GET", "POST"])
def loggin():
    username=request.form.get("username")
    password=request.form.get("password")

    if request.method == "POST":
        user= {}
        if os.path.exists("user.json"):
            with open("user.json") as user_file:
                user=json.load(user_file)
        if request.form['username'] in user.keys():
            return "Username already taken!, take another one"

        user[request.form["username"]] = {'password':request.form['password']}
        with open("user.json", "w") as user_file:
            json.dump(user, user_file)
        return render_template("loggin.html")

@app.route("/connect", methods=["GET", "POST"])
def connect():
    username=request.form.get("username1")
    password=request.form.get("password1")

    if request.method == "POST":
        with open("user.json") as user_file:
            user=json.load(user_file)
            for i in user:
                if request.form["username1"] in user.keys():
                    return "ok"
                else:
                    return render_template("error.html")
