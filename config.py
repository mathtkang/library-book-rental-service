import os

# 현재 모듈이 위치한 디렉토리 경로 반환 (폴더 구조가 달라져도, 현재 폴더를 가져와서 사용할 수 있도록)
BASE_DIR = os.path.dirname(__file__)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask:devpassword@localhost:3306/library'
    # {데이터베이스에 접속할 드라이버}://{사용자이름}:{사용자비밀번호}@{DB호스트주소}:{portnumber}/{연결할DB이름}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_TRACK_MODIFICATIONS: SQLAlchemy의 트래킹 기능 / SQLAlchemy에서 모델 변경을 추적하지 않도록 설정 (SQLAlchemy의 성능 향상, 불필요한 데이터베이스 쿼리 줄여줌)