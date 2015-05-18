import pymongo, hashlib
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

#checks if length of post is greater than 0
def checkPost(postToCheck):
    return len(postToCheck) > 0

#adds a user to users if username and password are valid
def addUser(username, password):
    if ((not checkUsername(username)) or (not checkPassword(password))):
        return False
    else:
        newUser = {"username": username,"password": hashlib.sha512(password).hexdigest()}
        users.insert(newUser)
        return True

def validateUser(username, password):
    record = users.find({"username":username})
    if (record.count() != 1):
        return False
    else:
        return record[0]['password'] == hashlib.sha512(password).hexdigest()


def addPost(username, post):
    if ((checkPost(post) == False) or (users.find({"username":username}).count()<1)):
        return False
    else:
        newPost = {"username": username,"post": post}
        posts.insert(newPost)
        return True
        
def addPublicPost(username, post):
    return addPost(username, post, "Public")

def addPrivatePost(username, post):
    return addPost(username, post, "Private")

def getPosts(privacy):
    result = posts.find({'privacy': privacy})
    postList = []
    for post in result:
        miniPostList = []
        miniPostList.append(post['username'])
        miniPostList.append(post['post'])
        miniPostList.append(post['privacy'])
        postList.append(miniPostList)
    return postList
        
def getPublicPosts():
    return getPosts("Public")

def getPrivatePosts():
    return getPosts("Private")



