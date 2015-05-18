from flask import Flask, session, flash, redirect, render_template, request, url_for

import random
import database
import os
import pymongo

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=["GET","POST"])
@app.route('/login', methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if(database.validateUser(username,password) == False):
            error = "Invalid username or password."
            return redirect(url_for('login'))
        flash("You've logged in successfully.")
        session['username'] = request.form['username']
        return redirect(url_for('posts'))
    return render_template("login.html")

@app.route('/register', methods=["GET","POST"])
def register():
    error = None
    if request.method == "POST":
        if button == "Login":
            return redirect(url_for('login'))
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if not database.addUser(username,password):
            flash("Invalid username or password.")
            return redirect(url_for('signup'))
        flash("Great! You've registered! Now you can log in.")
        return redirect(url_for('login'))
    age = []
    for x in range(12, 66):
        age += [x]
    return render_template("register.html", age = age)

@app.route('/posts',methods=["GET","POST"])
def posts():
    posts = database.getPublicPosts()
    if 'username' in session:
        username = session['username']
        posts.append(database.getPrivatePosts())
    else:
        username = "Anonymous"
    return render_template("public.html", posts = posts, username = username)

@app.route('/posts/submit',methods=["GET","POST"])
def submit():
    if 'username' in session:
        if request.method == "POST":
            database.addPost(session['username'],request.form["post"])   
            return redirect(url_for(request.form["type"])) 
        return render_template("submit.html") 
    flash("You are not logged in")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    error = None
    session.pop('username', None)
    flash("You've successfully logged out")
    return redirect(url_for('login'))    

if __name__ == '__main__':
    app.debug = True
    app.run()
