

import userRead
from mysql.connector import Error
from common import whereClause, updateClause
from datetime import datetime
class userWrite(userRead.userRead):

    def __init__(self, myWriteCursor=None, myReadCursor=None):

        if myReadCursor is None or myWriteCursor is None:
            raise Exception("No Cursor Exception")

        super(userWrite, self).__init__(myReadCursor=myReadCursor)
        self.myWriteCursor = myWriteCursor


    def formatEscapeChars(self, dItem=None):

        if dItem is None:
            raise Exception("Cannot format None")


        dTmp = dItem
        for k, v in dItem.items():
            if not isinstance(v, str):
                continue
                
            v.replace("\\", "U+005C")
            v.replace("'", "U+0027")
            v.replace('"', "U+003C")

            dTmp[k] = v

        dItem = dTmp
        return dItem

    def iUpdate(self, sQuery=None):

        try:

            self.myWriteCursor.execute(sQuery)
        except Error:
            raise

    def insertSingleton(self, dInsert=None):

        

        sQuery = """
        INSERT INTO user (userRef,username,password,dateCreated)
        VALUES (%s,%s,%s,%s)
        """

        dInsert=self.formatEscapeChars(dInsert)
        defaultRow = self.setDefaultRow(sKey=None)

        defaultRow.update(dInsert)
        dInsert = defaultRow
        dInsert["dateCreated"] = datetime.now()

        try:

            nextPK = self.getNextPK() + 10
            dInsert["userRef"] = nextPK
            
            self.myWriteCursor.execute(
                sQuery,
                (dInsert["userRef"],dInsert["username"],dInsert["password"],dInsert["dateCreated"])
            )
        except Error:
            raise


    def insertMultiple(self, lInserts=None):

        

        sQuery = """
        INSERT INTO user (userRef,username,password,dateCreated)
        VALUES (%s,%s,%s,%s)
        """

        lPrepInsert = []
        for dInsert in lInserts:

            if self.__dDefaultRow:
                defaultRow = self.__dDefaultRow.copy()
            else:
                defaultRow = self.setDefaultRow(sKey=None)

            defaultRow.update(dInsert)
            dTmp = defaultRow

            dTmp = self.formatEscapeChars(dItem=dTmp)

            dTmp["dateCreated"] = datetime.now()

            dTmp["userRef"] = self.nextPK + 10
            self.nextPK += 10
            
            lPrepInsert.append((dInsert["userRef"],dInsert["username"],dInsert["password"],dInsert["dateCreated"]))

        try:
            self.myWriteCursor.executemany(
                sQuery,
                lPrepInsert
            )
        except Error:
            raise



    def updateNextPK(self, iNextPK=0):

        if not iNextPK or not isinstance(iNextPK, int):
            raise Exception("Must provide PK > 0 to be next PK")

        try:
            sQuery = f"""
            UPDATE suser 
            SET suserRef = {iNextPK}
            """

            self.iUpdate(sQuery=sQuery)
        except Error:
            raise 

    def updateuser(self, dCriteria=None, dNewValues=None):    

        if dNewValues is None or dCriteria is None:
            raise Exception("Must have criteria and values to update")

        
        sQuery = """
        UPDATE user
        """

        sQuery += updateClause.getUpdateClause(dNewValues)
        sQuery += whereClause.getWhereClause(dCriteria)

        self.iUpdate(sQuery=sQuery)


