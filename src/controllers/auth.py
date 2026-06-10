from flask import Blueprint, request
from src.app import User, db
from flask_jwt_extended import create_access_token
from http import HTTPStatus

app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity="python")
    return {"access_token": access_token}
