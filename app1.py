from flask import Flask, render_template, session, flash, redirect, request, url_for

import random
import database
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    age = []
    for x in range(12, 66):
        age += [x]
    return render_template("register.html", age = age)

if __name__ == "__main__":
   app.debug = True
   app.run(host="0.0.0.0", port=8000)
