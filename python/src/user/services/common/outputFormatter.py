

def formatFetch(sTable="", dRows=None):

    outDict = {}

    outDict[sTable] = []

    for val in dRows.values():
        outDict[sTable].append(val)

    return outDict
