from flask import Flask
from app import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # 책이름
    publisher = db.Column(db.String(255))  # 출판사
    author = db.Column(db.String(255))  # 저자
    publication_date = db.Column(db.DateTime)  # 출간일
    pages = db.Column(db.Integer)  # 페이지 수
    isbn = db.Column(db.String(30))  # ISBN 코드
    description = db.Column(db.Text)  # 책 소개
    star = db.Column(db.Integer)  # 별점
    img_link = db.Column(db.String(255))  # 이미지
    rental_val = db.Column(db.Integer)  # 총 대여 횟수
    remaining = db.Column(db.Integer)  # 재고

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Rent(db.Model):
    __tablename__ = 'rent'

    id = db.Column(db.Integer, primary_key=True)
    rental_date = db.Column(db.DateTime, default=datetime.utcnow())  # 대여 일자
    due_date = db.Column(db.DateTime)  # 반납 예정 일자
    returned = db.Column(db.Boolean, default=False)  # 책이 반납되었는지 여부
    rental_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # FK
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)  # FK

    rental_user = db.relationship('User', foreign_keys=[rental_user_id])  # User 테이블과의 관계 정의
    book = db.relationship('Book', foreign_keys=[book_id])  # Book 테이블과의 관계 정의

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)  # 댓글 내용
    rating = db.Column(db.Integer, nullable=False)  # 평가 별점
    write_time = db.Column(db.DateTime, default=datetime.utcnow())  # 작성 시간
    written_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # FK
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)  # FK

    written_user = db.relationship('User', foreign_keys=[written_user_id])  # User 테이블과의 관계 정의
    book = db.relationship('Book', foreign_keys=[book_id])  # Book 테이블과의 관계 정의