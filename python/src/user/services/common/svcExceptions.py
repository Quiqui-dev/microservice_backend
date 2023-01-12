

class InsertException(Exception):

    def __init__(msg="", error=None):

        super(InsertException).__init__(msg=msg)


class EntryExists(Exception):
    pass

