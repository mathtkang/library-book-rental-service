import csv
from datetime import date, datetime

from db_connect import db
from models import LibraryBook

session = db.session

with open('library.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # img_link 수정
        img_link = f"/static/img_book/{row['id']}"
        try:
            open(f'{img_link}.png')
            img_link += '.png'
        except:
            img_link += '.jpg'

        # publication_date 수정
        publication_date = datetime.strptime(
            row['publication_date'], '%Y-%m-%d').date()

        libraryBook = LibraryBook(
            id=int(row['id']),
            book_name=row['book_name'],
            publisher=row['publisher'],
            author=row['author'],
            publication_date=publication_date,
            pages=int(row['pages']),
            isbn=row['isbn'],
            description=row['description'],
            star=0,
            img_link=img_link,
            rental_val=0,
            remaining=5,
        )
        db.session.add(libraryBook)
    db.session.commit()
