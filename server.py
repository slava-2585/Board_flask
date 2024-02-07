import os
from datetime import datetime

from flask import Flask, request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from model import User, Session, Advertisement

app = Flask('app')

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
        with Session() as session:
            if adv_id is None:
                advs = session.query(Advertisement).all()
                return jsonify({'Advert': [adv.to_json for adv in advs]})
            else:
                adv = session.get(Advertisement, adv_id)
                if adv is None:
                    raise HttpError(404, "Advertisement not found")
                return jsonify(adv)


    def post(self):
        with Session() as session:
            data = request.json
            adv = Advertisement(**data)
            session.add(adv)
            session.commit()
            return jsonify({'id': adv.id})

    def delete(self, adv_id):
        adv = get_adv_by_id(adv_id)
        self.session.delete(adv)
        self.session.commit()
        return jsonify({"status": "deleted"})

    def patch(self, adv_id):
        adv = get_adv_by_id(adv_id)
        data = request.json
        for field, value in data.item():
            setattr(adv, field, value)
        try:
            self.session.add(adv)
            self.session.commit()
        except IntegrityError:
            raise HttpError(409, "user already exists")
        return jsonify(adv)



# Пользователи
class UserCreate(MethodView):
    @property
    def session(self) -> Session:
        return request.session
    
    def get(self, user_id=None):
        with Session() as session:
            if user_id is None:
                users = session.query(User).all()
                return jsonify({'Users': [user.to_json for user in users]})
            else:
                user = get_user_by_id(user_id)
                return jsonify(user.to_json)

    def post(self):
        with Session() as session:
            data = request.json
            user = User(**data)
            session.add(user)
            session.commit()
            return jsonify({'id': user.id})

    def DELETE(self, user_id):
        user = get_adv_by_id(user_id)
        self.session.delete(user)
        self.session.commit()
        return jsonify({"status": "deleted"})

    def PATCH(self):
        pass


user_create = UserCreate.as_view('user_create')
adv_view = Advert.as_view('adv_view')
app.add_url_rule('/user/', view_func=user_create, methods=['GET', 'POST'])
app.add_url_rule('/user/<int:user_id>/', view_func=user_create, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/adv/', view_func=adv_view, methods=['GET', 'POST'])
app.add_url_rule('/adv/<int:adv_id>/', view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
