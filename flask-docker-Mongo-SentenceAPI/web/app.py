'''

Regestration of a user
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence from our datase for 1 token



'''


#Register
#Store
#Retrive

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
import bcrypt

from pymongo import MongoClient


app  = Flask(__name__)
api  = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["users"]


class Regestration(Resource):
    def post(self):
        #Step 1 is to get the posted data by users
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"]

        #hash(Abc123 + salt) = adafdklaj;dlkajdlka
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        #Store the username and pw into  SentencesDatabase
        users.insert_one({
            "username" : username,
            "password" : hashed_pw,
            "sentence" : "",
            "tokens" : 6
        }
        )

        retJson = {
            "status" : 200,
            "msg" : "You have successfully signed up for the API"
        }

        return retJson

def Verifypw(username, password):
    hashed_pw = users.find({
        "username" : username
    })[0]["password"]

    # hashed_pw = list(cursor)[0]["password"]

    if bcrypt.hashpw(password.encode("utf8"),hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "username" : username
        })[0]["tokens"]
        
    return tokens

class Store(Resource):
    def post(self):
        #Step1 : Get the posted Data
        postedData = request.get_json()


        #Step2 : read the data from the request
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Step3 : Verify the username and pw match
        correct_pw = Verifypw(username, password)

        if not correct_pw:
            retJson = {
                "status" : 302
            }

            return retJson

        #Step4 : Verify if the user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status" : 302
            }
            return retJson


        #Step5 : Store the sentence, take one token away and return 200
        users.update_one({
            "username" : username
        },
        {
            "$set":{
                "sentence" : sentence,
                "tokens" : num_tokens-1
            }
        })
        retJson = {
            "status" : 200,
            "msg" : "Sentence saved successfully"
        }

        return retJson
    
class Retrieve(Resource):
    def get(self):
        postedData = request.get_json()

        #Step2 : read the data from the request
        username = postedData["username"]
        password = postedData["password"]

        #Step3 : Verify the username and pw match
        correct_pw = Verifypw(username, password)

        if not correct_pw:
            retJson = {
                "status" : 302
            }

            return retJson

        #Step4 : Verify if the user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status" : 302
            }
            return retJson
        
        sentence = users.find({
            "username" : username
        })[0]["sentence"]

        retJson = {
            "status" :200,
            "sentence" : str(sentence)
        }

        return retJson




api.add_resource(Regestration,"/register")
api.add_resource(Store,"/store")
api.add_resource(Retrieve,"/retrieve")






if __name__ == "__main__":
    app.run("0.0.0.0")


'''
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os

from pymongo import MongoClient


app  = Flask(__name__)
api  = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert_one({
    'num_of_users' : 0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        new_num = prev_num + 1
        UserNum.update_one({},{"$set":{"num_of_users" : new_num}})
        return str("Hello user " + str(new_num))


def checkPostedData(postedData, funcName):
    if (funcName == "add" or funcName == "subtract" or funcName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #missing parameter
        else:
            return 200
    elif (funcName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #missing parameter
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200



class Add(Resource):
    def post(self):
        #If I am here, then the resource Add was requested using the Method Post

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify Validity of posted data
        status_code = checkPostedData(postedData,"add")
        if (status_code != 200):
            retJson = {
                "Message" : "An error happened",
                "Status Code" : status_code
            }
            return retJson

        #If I am here, the status_code=200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Add posted data:
        ret = x+y
        retMap = {
            "Message" : ret,
            "Status code" : 200
        }
        return retMap


class Subtract(Resource):
    def post(self):
        #If I am here, then the resource Subtract was requested using the Method Post

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify Validity of posted data
        status_code = checkPostedData(postedData,"subtract")
        if (status_code != 200):
            retJson = {
                "Message" : "An error happened",
                "Status Code" : status_code
            }
            return retJson

        #If I am here, the status_code=200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Subtract posted data:
        ret = x-y
        retMap = {
            "Message" : ret,
            "Status code" : 200
        }
        return retMap

class Multiply(Resource):
    def post(self):
        #If I am here, then the resource Multiply was requested using the Method Post

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify Validity of posted data
        status_code = checkPostedData(postedData,"multiply")
        if (status_code != 200):
            retJson = {
                "Message" : "An error happened",
                "Status Code" : status_code
            }
            return retJson

        #If I am here, the status_code=200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply posted data:
        ret = x*y
        retMap = {
            "Message" : ret,
            "Status code" : 200
        }
        return retMap

class Divide(Resource):
    def post(self):
        #If I am here, then the resource Divide was requested using the Method Post

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify Validity of posted data
        status_code = checkPostedData(postedData,"division")
        if (status_code != 200):
            retJson = {
                "Message" : "An error happened",
                "Status Code" : status_code
            }
            return retJson

        #If I am here, the status_code=200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Divide posted data:
        ret = x/y
        retMap = {
            "Message" : ret,
            "Status code" : 200
        }
        return retMap

api.add_resource(Add,"/add")
api.add_resource(Subtract,"/subtract")
api.add_resource(Multiply,"/multiply")
api.add_resource(Divide,"/division")
api.add_resource(Visit,"/visit")



@app.route("/")
def hello_world():
    return "Hello World!"




if __name__ == "__main__":
    app.run("0.0.0.0")

'''