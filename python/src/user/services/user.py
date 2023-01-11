from flask import request, current_app
from baseClasses.user import User
from common.responseGenerator import responseHandler


def getAllUsers():

    return "all users"

def getUser():
    
    if not request.json:
        return responseHandler("failed", 400, "failed to fetch data", "No filters to fetch on")
    
    return "user"

def addUser():

    return "successfully added new user"

def updateUser():

    return "successfully updated user"

def deleteUser():

    return "successfully deleted user"