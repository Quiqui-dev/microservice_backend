

def responseHandler(status="success", code=200, message="Operation was successful", detail=None):

    return {"status": status, "code": code, "message": message, "detail": detail}
    