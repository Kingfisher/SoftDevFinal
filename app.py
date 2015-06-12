from flask import Flask, session, flash, redirect, render_template, request, url_for

import random
import database
import os
import pymongo

from uuid import uuid4
from datetime import datetime, timedelta

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from pymongo import MongoClient

class MongoSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False


class MongoSessionInterface(SessionInterface):

    def __init__(self, host='localhost', port=27017,
                 db='', collection='sessions'):
        client = MongoClient(host, port)
        self.store = client[db][collection]

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if sid:
            stored_session = self.store.find_one({'sid': sid})
            if stored_session:
                if stored_session.get('expiration') > datetime.utcnow():
                    return MongoSession(initial=stored_session['data'],
                                        sid=stored_session['sid'])
        sid = str(uuid4())
        return MongoSession(sid=sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        if self.get_expiration_time(app, session):
            expiration = self.get_expiration_time(app, session)
        else:
            expiration = datetime.utcnow() + timedelta(hours=1)
        self.store.update({'sid': session.sid},
                          {'sid': session.sid,
                           'data': session,
                           'expiration': expiration}, True)
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=self.get_expiration_time(app, session),
                            httponly=True, domain=domain)

app = Flask(__name__)
app.session_interface = MongoSessionInterface(db='pjuu')
app.secret_key = os.urandom(24)

@app.route('/',methods=["GET","POST"])
def default():
    return redirect(url_for('posts'))

@app.route('/posts',methods=["GET","POST"])
def posts():
    posts = database.getPublicPosts() + database.getPrivatePosts()
    if request.method == "POST":
        button = request.form["b"]
        if button == "deletePosts":
            print "Cats dance."
            database.removePosts()
            flash("You've successfully removed all posts.")
        if button == "deleteUsers":
            database.removeUsers()
            flash("You've successfully removed all users other than yourself.")
        return redirect(url_for('posts'))
    else:
        if 'username' in session:
            username = session['username']
        else:
            username = False
        return render_template("posts.html", posts = posts, username = username)     

'''@app.route('/posts/<id>',methods=["GET","POST"])
def posts(id):
    post = database.findPost(id)
    username = post[0]
    postContent = post[1]
    privacy = post[2]
    if 'username' not in session:
        if privacy=="private":
            flash("You must be logged in to view this")
            session['goTo'] = str(id)
            return redirect(url_for('login'))
    return render_template("post.html", username=username, postContent=postContent, privacy=privacy)'''

@app.route('/posts/submit',methods=["GET","POST"])
def submit():
    if 'username' in session:
        username = session['username']
        if request.method == "POST":
            post = request.form["post"]
            postType = request.form["privacy"]
            if(database.checkPosts()):
                postId = 1
            else:
                postId = checkPosts()
            database.addPost(username, post, postType, postId = postId) 
            return redirect(url_for('posts')) 
        return render_template("submit.html", username = username) 
    else:
        flash("You are not logged in")
        session['goTo'] = 'submit'
        return redirect(url_for('login'))


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
            session['username'] = request.form['username']
            if 'goTo' in session:
                goTo = session['goTo']
                session.pop('goTo')
                return redirect(url_for(goTo))
            else:
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
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            #Register unsuccessful, return to signup
            if not database.addUser(username,password,email):
                flash("Invalid username, password, or email address.")
                return redirect(url_for('register'))
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

