from accessClasses import userRead, userWrite
from common import svcExceptions, outputFormatter
from datetime import datetime

class User:

    def __init__(self, readCursor=None, writeCursor=None):

        self.uRead = None
        self.uWrite = None

        self.readCursor = readCursor
        self.writeCursor = writeCursor

    def addUser(self, userData):

        # validate data, call userWrite to insert and then check the insert was successful.

        if self.uWrite is None:

            self.uWrite = userWrite.userWrite(myWriteCursor=self.writeCursor, myReadCursor=self.readCursor)

        
        # check if user with username already exists and raise if it does

        try:
            self.uWrite.set_userRows(dCriteria={"username": userData["username"]})
            raise svcExceptions.EntryExists(f"username: {userData['username']} already exists")            
        except svcExceptions.EntryExists:
            raise
        except:
            pass

        
        # try to insert the user.

        self.uWrite.insertSingleton(dInsert=userData)



    def fetchUser(self, userFilters=None):

        # given some filters fetch a user, if none given fetch the first entry. (will be managed properly)

        if "password" in userFilters:
            userFilters.pop("password")

        try:
            if self.uRead is None:
                self.uRead = userRead.userRead(myReadCursor=self.readCursor)
            
            self.uRead.set_userRows(dCriteria=userFilters)
            dUserRows = self.uRead.getuserRows()

            return outputFormatter.formatFetch(sTable="user", dRows=dUserRows)
        except:
            raise
        

    def updateUser(self, userData):
        
        # given a user pk and data to update, after validation update the record.
        pass




    
