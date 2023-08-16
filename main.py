from app import create_app
from app import db
from config import Config

app = create_app(config_class=Config)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8088)