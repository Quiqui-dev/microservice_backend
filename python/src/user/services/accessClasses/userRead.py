

from common import whereClause
class userRead:

    def __init__(self, myReadCursor=None):

        if myReadCursor is None:
            raise Exception("No Cursor Exception")

        self.myReadCursor = myReadCursor

        self.__duserRows = {}
        self.__dDefaultRow = {}
        self.__iRowCount = 0
        self.nextPK = 0


    def getRows(self):
        return self.__duserRows

    def setRowCount(self, numRows):
        self.__iRowCount = numRows

    def getRowCount(self):
        return self.__iRowCount

    
    def removeEscapeChars(self, dItem=None):

        if dItem is None:
            raise Exception("cannot format None")

        dTmp = dItem
        for k,v in dItem.items():
            if not isinstance(v, str):
                continue

            v.replace("U+005C", " \\")
            v.replace("U+0027", "'")
            v.replace("U+003C", '"')

            dTmp[k] = v 

        dItem = dTmp
        return dItem

    def iSelect(self, sQuery, sKey=None):

        self.myReadCursor.execute(sQuery)
        rows = self.myReadCursor.fetchall()
        rowcount = self.myReadCursor.rowcount


        if not self.myReadCursor.rowcount:
            raise Exception("No Rows Found")


        if sKey is None:

            iCount = 0

            for row in rows:

                # index the rows from 0 -> n-1

                dTmp = self.removeEscapeChars(row)
                self.__duserRows[iCount] = dTmp
                iCount += 1

        else:

            try:

                for row in rows:
                    # index the rows by a column in the result set
                    dTmp = self.removeEscapeChars(row)
                    self.__duserRows[row[sKey]] = dTmp

                    iCount += 1

            except:
                raise Exception(f"No column matching {sKey}")

        
        if iCount != rowcount:
            raise Exception("Row count mismatch")


        self.setRowCount(iCount)

        return iCount

    def set_userRows(self, dCriteria=None, sKey=None):

        
        try:
            self.removeEscapeChars(dItem=dCriteria)

            
            sQuery = """
            SELECT userRef,username,password,dateCreated
            FROM user
            """
            sQuery += whereClause.getWhereClause(dCriteria=dCriteria)


            self.iSelect(sQuery=sQuery, sKey=sKey)
        except:
            raise Exception("failed to fetch")

        
        return self.__duserRows

    def setDefaultRow(self, sKey=None):

        try:
            
            sQuery = """
            SELECT userRef,username,password,dateCreated
            FROM user
            WHERE userRef = 0
            """


            self.iSelect(sQuery=sQuery, sKey=sKey)
            self.__dDefaultRow = self.__duserRows

            self.__duserRows = {}

            return self.__dDefaultRow
        except:
            raise Exception("could not fetch default row")

    def setFreeQueryRows(self, sQuery=None, sKey=None):

        # should likely validate the query to ensure it is safe but let's let the dev worry about it

        if sQuery is None:
            raise Exception("Query must be supplied to execute")

        self.iSelect(sQuery=sQuery, sKey=sKey)
        
        return self.__duserRows

    def getNextPK(self):

        sQuery = """
        SELECT * FROM suser
        """

        self.iSelect(sQuery=sQuery, sKey=None)
        self.__dDefaultRow = self.__duserRows
        self.nextPK = self.__duserRows[0]["suserRef"]

        return self.__duserRows[0]["suserRef"]
        

