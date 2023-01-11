from accessClasses import userRead, userWrite


class User:

    def __init__(self, readCursor=None, writeCursor=None):

        self.uRead = None
        self.uWrite = None

        self.readCursor = readCursor
        self.writeCursor = writeCursor

    def addUser(self, userData):

        # validate data, call userWrite to insert and then check the insert was successful.
        pass

    def fetchUser(self, userFilters=None):

        # given some filters fetch a user, if none given fetch the first entry. (will be managed properly)
        pass

    def fetchUsers(self, filters=None):

        # given filters return users which match the criteria/ if no filters return all users
        pass

    def updateUser(self, userData):
        
        # given a user pk and data to update, after validation update the record.
        pass




    
