# 기본 이미지 선택
FROM python:3.9

RUN apt-get update && apt-get install -y nginx

COPY . /app

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
RUN pip install -r requirements.txt

# 실행 명령 설정
CMD ["python", "main.py"]
