from flask import Flask
from db_connect import db
from models import *
import config
from models import LibraryUser, LibraryBook, LibraryReview, UserRentBook


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    # 블루프린트
    from views import book_detail_api, main_api, mypage_api, user_api
    app.register_blueprint(book_detail_api.bp)
    app.register_blueprint(main_api.bp)
    app.register_blueprint(mypage_api.bp)
    app.register_blueprint(user_api.bp)

    # 세션 사용을 위해서
    app.secret_key = "secret_key_for_session"
    app.config['SESSION_TYPE'] = 'filesystem'

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=8088)
