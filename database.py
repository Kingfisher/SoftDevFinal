import pymongo, hashlib
from bson.json_util import dumps

connection = pymongo.MongoClient()

db = connection["database"]
users = db.users
posts = db.posts


#return true if password's length is greater than 0
def checkPassword(passwordToCheck):
    return len(passwordToCheck) > 0

#returns true if username has length greater than one and is not taken already
def checkUsername(usernameToCheck):
    return ((len(usernameToCheck) > 0) and (users.find({"username":usernameToCheck}).count() == 0))

#checks if email address has minimum length of six with @, ., and with at least one character for the email and three for the ending
def checkEmail(email):
    if (len(email) > 6):
        if (email.find('@') == 1):
            if (email.find('.') == 1):
                return True
    return False

#checks if length of post is greater than 0
def checkPost(postToCheck):
    return len(postToCheck) > 0

#adds a user to users if username and password are valid
def addUser(username, password, email):
    if ((not checkUsername(username)) or (not checkPassword(password))):
        #if (not checkEmail(email)):
        return False
    else:
        newUser = {"username": username,"password": hashlib.sha512(password).hexdigest(), "email" : email}
        users.insert(newUser)
        return True

#checks whether user exists, then checks if passwords match
def validateUser(username, password):
    record = users.find({"username":username})
    if (record.count() != 1):
        return False
    else:
        return record[0]['password'] == hashlib.sha512(password).hexdigest()

#finds a post
def findPost(id):
    record = users.find({"id":id})
    return record[0]

#checks if posts are empty, and if not, returns the last id used plus one
def checkPosts():
    if(posts.count() == 0):
        return True
    else:
        print list(posts.find())[-1]
        print "ADSFADSFAD"
        return list(posts.find())[-1]["post"]

#adds a post
def addPost(username, title, post, privacy, postId, timeStamp):
    if ((checkPost(post) == False) or (users.find({"username":username}).count() < 1)):
        return False
    else:
        newPost = {"username": username, "title" : title, "post": post, "privacy" : privacy, "postId" : postId, "timeStamp" : timeStamp, "comments" : {}}  
        posts.insert(newPost)
        return True
    

#removes a post by id
def removePost(id):
    if(posts.find({"id":id}).count() < 1):
        return False
    else:
        posts.remove(posts.find_one({"id":id}))
        return True

#remove all posts
def removePosts():
    db.posts.remove({})
    posts = db.posts

#removes all users
def removeUsers():
    db.users.remove({})
    users = db.users
    addUser("a","9138","a@a.org")
        
#adds a publicly available post
def addPublicPost(username, post):
    return addPost(username, post, "public")

#adds a members only post
def addPrivatePost(username, post):
    return addPost(username, post, "private")

#returns a list of lists, each of a post with one type of privacy, with the username, post, and privacy contained 
def getPosts(privacy):
    ###print "Test", dumps(posts.find({}))
    ###print "database: ", posts.find({'privacy': privacy})
    result = posts.find({"privacy": privacy})
    postList = []
    for post in result:
        miniPostList = []
        miniPostList.append(post['username'])
        miniPostList.append(post['title'])
        miniPostList.append(post['post'])
        miniPostList.append(post['privacy'])
        miniPostList.append(post['timeStamp'])
        postList.append(miniPostList)
    return postList

#gets a list of public posts
def getPublicPosts():
    return getPosts("public")

#gets a list of private posts
def getPrivatePosts():
    return getPosts("private")



