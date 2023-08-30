# 기본 이미지 선택
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install --no-cache-dir poetry

# pyproject.toml 및 poetry.lock 복사
COPY pyproject.toml poetry.lock /app/

# 의존성 설치
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# 프로젝트 파일 복사
COPY . /app/

# 실행 명령 설정
CMD ["poetry", "run", "gunicorn", "--workers", "4", "--bind", "0.0.0.0:8088", "main:app"]
