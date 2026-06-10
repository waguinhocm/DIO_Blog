from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import inspect
from src.app import User, db
from http import HTTPStatus

app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()


def _list_user():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    return [
        {
            "id": user.id,
            "username": user.username,
        }
        for user in users
    ]


@app.route("/", methods=["GET", "POST"])
@jwt_required()
def list_or_create_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"identity": get_jwt_identity(), "users": _list_user()}


@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }


@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    return {
        "id": user.id,
        "username": user.username,
    }


@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
