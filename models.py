from db_connect import db
from datetime import datetime

'''
[데이터베이스 제약 조건 명시 파일]
관계형 데이터베이스의 데이터를 객체랑 연결 시켜주는 것을 ORM (Object Relational Mapping)이라 한다.
즉, 외부에 존재하는 DB를 서버에서 사용하기 위해, DB와 동일한 제약조건을 객체에 부여하는 파일이다.
테이블명 : 객체 이름과 달라도 되지만, 외부 테이블에서 호출시 이름으로 사용(소문자로 시작)
'''


# 도서관 사용자 테이블
class LibraryUser(db.Model):

    __tablename__ = 'libraryUser'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, user_name, user_email, password):
        self.user_name = user_name
        self.user_email = user_email
        self.password = password


# 도서관 전체 책 목록 테이블
class LibraryBook(db.Model):

    __tablename__ = 'libraryBook'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_name = db.Column(db.String(255))  # 책이름
    publisher = db.Column(db.String(255))  # 출판사
    author = db.Column(db.String(255))  # 저자
    publication_date = db.Column(db.Date)  # 출간일
    pages = db.Column(db.Integer)  # 페이지 수
    isbn = db.Column(db.String(30))  # ISBN 코드
    description = db.Column(db.Text)  # 책 소개
    star = db.Column(db.Integer)  # 별점
    img_link = db.Column(db.String(255))  # 이미지
    rental_val = db.Column(db.Integer)  # 총 대여 횟수
    remaining = db.Column(db.Integer)  # 재고


# 책 대여 현황 테이블
class UserRentBook(db.Model):
    __tablename__ = 'userRentBook'

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'libraryBook.id'), nullable=False)
    rental_date = db.Column(db.Date)  # 대여 일자
    return_date = db.Column(db.Date)  # 반납 일자
    book_data = db.relationship(
        'LibraryBook', foreign_keys='UserRentBook.book_id')  # UserRentBook 테이블과 LibraryBook 연결해주는 변수 (LibraryBook의 속성을 가져와 쓸 수 있도록 해준다. 새로운 컬럼이 추가되는게 아니다. 연결해주는 변수일 뿐!)

    def __init__(self, user_email, book_id, rental_date):
        self.user_email = user_email
        self.book_id = book_id
        self.rental_date = rental_date


# 책 소개 페이지의 댓글 테이블
class LibraryReview(db.Model):
    __tablename__ = 'libraryReview'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)  # 댓글 내용
    rating = db.Column(db.Integer, nullable=False)  # 평가 별점
    write_time = db.Column(db.DateTime, default=datetime.utcnow())  # 작성 시간
    book_id = db.Column(db.Integer, db.ForeignKey(
        'libraryBook.id'), nullable=False)

    def __init__(self, user_name, user_email, content, rating, book_id, write_time):
        self.user_name = user_name
        self.user_email = user_email
        self.content = content
        self.rating = rating
        self.write_time = write_time
        self.book_id = book_id


if __name__ == "__main__":
    db.create_all()
