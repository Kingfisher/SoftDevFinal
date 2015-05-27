from flask import Flask, session, flash, redirect, render_template, request, url_for

import random
import database
import os
import pymongo

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=["GET","POST"])

@app.route('/posts',methods=["GET","POST"])
def posts():
    posts = database.getPublicPosts()
    if 'username' in session:
        username = session['username']
        posts.append(database.getPrivatePosts())
    else:
        username = False
    return render_template("posts.html", posts = posts, username = username)

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        button = request.form["b"]
        if button == "Register":
            return redirect(url_for('register'))
        elif button == "Posts":
            return redirect(url_for('posts'))
        else:
            username = request.form["username"]
            password = request.form["password"]
            #Login unsuccessful, return to login
            if(database.validateUser(username,password) == False):
                flash("Invalid username or password.")
                return redirect(url_for('login'))
            #Login successful, redirect to main page
            flash("Login successful.")
            session['username'] = request.form['username']
            return redirect(url_for('posts'))
    return render_template("login.html")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        button = request.form["b"]
        if button == "Login":
            return redirect(url_for('login'))
        elif button == "Posts":
            return redirect(url_for('posts'))
        else:
            button = request.form["b"]
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            #Register unsuccessful, return to signup
            if not database.addUser(username,password,email):
                flash("Invalid username or password.")
                return redirect(url_for('signup'))
            #Register successful, redirect to login
            flash("Great! You've registered! Now you can log in.")
            return redirect(url_for('login'))
    else:
        age = []
        for x in range(12, 66):
            age += [x]
        return render_template("register.html", age = age)

@app.route("/user/<username>",methods=["GET","POST"])
def user(username):
    if request.method=="GET":
        return render_template("user.html", username = username)
    else:
        return render_template("user.html", username = username)

@app.route('/posts/submit',methods=["GET","POST"])
def submit():
    if 'username' in session:
        if request.method == "POST":
            database.addPost(session['username'],request.form["post"])   
            return redirect(url_for(request.form["type"])) 
        return render_template("submit.html", username = session['username']) 
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('_flashes', None)
        flash("You've successfully logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    app.run()

