import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 현재 모듈이 위치한 디렉토리 경로 반환 (폴더 구조가 달라져도, 현재 폴더를 가져와서 사용할 수 있도록)
BASE_DIR = os.path.dirname(__file__)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    
    PERMANENT_SESSION_LIFETIME = 60 * 30  # 30min