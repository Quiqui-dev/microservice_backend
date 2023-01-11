import validate, json 

def get_access(request):

    has_access, err = validate.token(request)

    if err:
        return err

    has_access = json.loads(has_access)
    return has_access