import os

# 폴더 구조가 달라져도, 현재 폴더를 가져와서 사용할 수 있도록 설정
BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1124@localhost:3306/library'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 이걸 켜면 메모리 사용량이 늘어나서, 꺼주는게 좋아요.
