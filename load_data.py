import csv
from datetime import date, datetime

from app import create_app, db
from app.models import Book

app = create_app()  # Flask 애플리케이션 객체 생성
app.app_context().push()  # 애플리케이션 컨텍스트 설정

session = db.session

with open('library.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # img_link 수정
        img_link = f"/media/img_book/{row['id']}"
        try:
            open(f'{img_link}.png')
            img_link += '.png'
        except:
            img_link += '.jpg'

        # publication_date 수정
        publication_date = datetime.strptime(
            row['publication_date'], '%Y-%m-%d').date()

        book = Book(
            id=int(row['id']),
            name=row['book_name'],
            publisher=row['publisher'],
            author=row['author'],
            publication_date=publication_date,
            pages=int(row['pages']),
            isbn=row['isbn'],
            description=row['description'],
            star=0,
            img_link=img_link,
            remaining=5,
        )
        db.session.add(book)
    db.session.commit()
