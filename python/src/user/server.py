from flask import Flask, request, current_app
from auth_svc import access, validate
from services.common import conPool
import connexion

options = {"swagger_ui_config": {"displayOperationId": True}}
server = connexion.App(__name__, specification_dir="./schemas/")


server.add_api("user.json")


@server.route("/login", methods=["POST"])
def login():

    token, err = access.login(request)

    if err:
        return err
    
    return token


@server.route("/")
def hello_world():
    return "Hello World"



if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
    current_app.config["writePool"] = conPool.WritePool()