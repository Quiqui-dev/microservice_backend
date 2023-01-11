
def getWhereClause(dCriteria=None):

    if dCriteria is None:
        raise Exception("Empty where clause")

    sWhere = " WHERE"
    iCount = 0

    for k,v in dCriteria.items():

        if isinstance(v, str):
            sep = "'"
        else:
            sep = ""

        if not iCount:
            sWhere += f" {k} = {sep}{v}{sep}"
        else:
            sWhere += f" AND {k} = {sep}{v}{sep}"
        
        iCount += 1

    return sWhere


if __name__ == "__main__":

    dTest = {}

    dTest["column1"] = 1
    dTest["column2"] = "hello"

    print(getWhereClause(dCriteria=dTest))