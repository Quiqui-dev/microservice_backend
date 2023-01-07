import os, requests

def token(request):

    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)
    elif not request.headers["Authorization"]:
        return None, ("missing credentials", 401)

    bearer_token = request.headers["Authorization"]

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers= {"Authorization": bearer_token}
    )

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)
