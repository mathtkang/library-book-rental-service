from flask import Flask
from db_connect import db
from models import *
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    # 블루프린트
    from views import book_detail_api, book_list_api, main_api, rental_api, return_book_api, user_api
    app.register_blueprint(book_detail_api.bp)
    app.register_blueprint(book_list_api.bp)
    app.register_blueprint(main_api.bp)
    app.register_blueprint(rental_api.bp)
    app.register_blueprint(return_book_api.bp)
    app.register_blueprint(user_api.bp)

    # 세션 사용을 위해서
    app.secret_key = "asdfasdfasdf"
    app.config['SESSION_TYPE'] = 'filesystem'

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
