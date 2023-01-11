
def getUpdateClause(dNewVals=None):

    if dNewVals is None:
        raise Exception("Values must not be None")

    sUpdate = "SET"
    iCount = 0


    for k,v in dNewVals.items():

        if isinstance(v, str):
            sep= "'"
        else:
            sep = ""

        if iCount == len(dNewVals) - 1:
            sUpdate += f" {k} = {sep}{v}{sep}"
        else:
            sUpdate += f" {k} = {sep}{v}{sep},"

        iCount += 1

    return sUpdate

if __name__ == "__main__":

    dTest = {}

    dTest["column1"] = 1
    dTest["column2"] = "hello"

    print(getUpdateClause(dNewVals=dTest))