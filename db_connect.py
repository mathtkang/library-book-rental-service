from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask:devpassword@localhost:3306/library'
# {데이터베이스에 접속할 드라이버}://{사용자이름}:{사용자비밀번호}@{DB호스트주소}:{portnumber}/{연결할DB이름}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SQLALCHEMY_TRACK_MODIFICATIONS: SQLAlchemy의 트래킹 기능 / SQLAlchemy에서 모델 변경을 추적하지 않도록 설정 (SQLAlchemy의 성능 향상, 불필요한 데이터베이스 쿼리 줄여줌)

db = SQLAlchemy(app)