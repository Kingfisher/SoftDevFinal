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

#Checks whether user exists, then checks if passwords match
def validateUser(username, password):
    record = users.find({"username":username})
    if (record.count() != 1):
        return False
    else:
        return record[0]['password'] == hashlib.sha512(password).hexdigest()

#Adds a post
def addPost(username, post, privacy):
    if ((checkPost(post) == False) or (users.find({"username":username}).count() < 1)):
        return False
    else:
        newPost = {"username": username,"post": post, "privacy" : privacy}
        posts.insert(newPost)
        return True

#Removes a post by id
def removePost(id):
    if(posts.find({"id":id}).count() < 1):
        return False
    else:
        posts.remove(posts.find_one({"id":id}))
        return True

#Remove all posts
def removePosts():
    db.posts.remove({})
    posts = db.posts

#Removes all users
def removeUsers():
    db.users.remove({})
    users = db.users
        
#Adds a publicly available post
def addPublicPost(username, post):
    return addPost(username, post, "Public")

#Adds a members only post
def addPrivatePost(username, post):
    return addPost(username, post, "Private")

#Returns a list of lists, each of a post with one type of privacy, with the username, post, and privacy contained 
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
        
#Gets a list of public posts
def getPublicPosts():
    return getPosts("Public")

#Gets a list of private posts
def getPrivatePosts():
    return getPosts("Private")



