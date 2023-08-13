from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config_class=Config): 
    app = Flask(__name__)
    # app.debug = False  # [DEPLOY]시 디버그모드 비활성화 해줌
    
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.secret_key = Config.SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = Config.PERMANENT_SESSION_LIFETIME
    app.config['SESSION_TYPE'] = 'filesystem'  # session을 어떻게 저장할 것인지? (여기서는) 파일 시스템에 저장하겠다는 의미

    db.init_app(app)
    migrate = Migrate(app, db)  # migration시(flask db init) 이게 없으면 " Error: No such command 'db'. "가 나온다.
    
    from app.views import auth, book_info, main, user
    app.register_blueprint(auth.bp)
    app.register_blueprint(book_info.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(user.bp)

    return app

