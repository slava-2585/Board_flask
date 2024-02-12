import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from schema import CreateUser, UpdateAdv, CreateAdv

from model import User, Session, Advertisement

load_dotenv()
app = Flask('app')
jwt = JWTManager(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


def validate_json(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)

def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def get_adv_by_id(adv_id: int):
    adv = request.session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, "Advertisement not found")
    return adv


# Объявления---------------------
class Advert(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, adv_id):
        if adv_id is None:
            advs = self.session.query(Advertisement).all()
            return jsonify({'Advert': [adv.to_json for adv in advs]})
        else:
            adv = self.session.get(Advertisement, adv_id)
            if adv is None:
                raise HttpError(404, "Advertisement not found")
            return jsonify(adv)

    @jwt_required()
    def post(self):
        data = validate_json(CreateAdv, request.json)
        user_id = get_jwt_identity()
        adv = Advertisement(creator=user_id, **data)
        self.session.add(adv)
        self.session.commit()
        return jsonify({'id': adv.id})

    @jwt_required()
    def delete(self, adv_id):
        user_id = get_jwt_identity()
        adv = self.session.query(Advertisement).filter(Advertisement.creator == user_id, Advertisement.id == adv_id).first()
        if adv is None:
            raise HttpError(404, "Advertisement not found")
        self.session.delete(adv)
        self.session.commit()
        return jsonify({"status": "deleted"})

    @jwt_required()
    def patch(self, adv_id):
        user_id = get_jwt_identity()
        adv = self.session.query(Advertisement).filter(Advertisement.creator == user_id, Advertisement.id == adv_id).first()
        data = validate_json(UpdateAdv, request.json)
        for field, value in data.items():
            setattr(adv, field, value)
        try:
            self.session.add(adv)
            self.session.commit()
        except IntegrityError:
            raise HttpError(409, "Advertisement already exists")
        return jsonify(adv.to_json)


# Пользователи ----------------------------------------------------------
# class UserCreate(MethodView):
#     @property
#     def session(self) -> Session:
#         return request.session
#
    # def get(self, user_id=None):
    #     with Session() as session:
    #         if user_id is None:
    #             users = session.query(User).all()
    #             return jsonify({'Users': [user.to_json for user in users]})
    #         else:
    #             user = get_user_by_id(user_id)
    #             return jsonify(user.to_json)
#
#     def DELETE(self, user_id):
#         user = get_adv_by_id(user_id)
#         self.session.delete(user)
#         self.session.commit()
#         return jsonify({"status": "deleted"})

# @app.route('/adv/', methods=['POST'])
# @jwt_required()
# def add_adv():
#     data = request.json
#     user_id = get_jwt_identity()
#     user_id = 3
#     adv = Advertisement(creator=user_id, **data)
#     with Session() as session:
#         session.add(adv)
#         session.commit()
#     return jsonify({'id': adv.id})


@app.route('/register/', methods=['POST'])
def register():
    with Session() as session:
        data = validate_json(CreateUser, request.json)
        user = User(**data)
        session.add(user)
        session.commit()
        token = user.get_token()
        return {'access_token': token}


@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    user = User.authenticate(**data)
    token = user.get_token()
    return {'access_token': token}


# user_create = UserCreate.as_view('user_create')
adv_view = Advert.as_view('adv_view')
# app.add_url_rule('/user/', view_func=user_create, methods=['GET', 'POST'])
# app.add_url_rule('/registration/', view_func=user_create, methods=['POST'])
# app.add_url_rule('/user/<int:user_id>/', view_func=user_create, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/adv/', view_func=adv_view, methods=['GET', 'POST'])
app.add_url_rule('/adv/<int:adv_id>/', view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
