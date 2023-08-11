from datetime import datetime
from flask import redirect, request, render_template, flash, url_for
from flask import Blueprint, session
from flask.views import MethodView

from app.models import User, Book, Rent, Review
from app import db

bp = Blueprint('main', __name__, url_prefix='/')


# @bp.route('/', methods=['GET', 'POST'])
class BookListView(MethodView):
    def get(self):
        '''
        Redirect page: main.html
        ✅ 도서관의 책 전체 리스트 반환
        '''
        book_list = Book.query.all()
        return render_template("main.html", book_list=book_list)

    def post(self):
        '''
        - 대여하기 버튼 클릭시 이미 빌린 도서는 마이페이지로 연동
        ✅ '자세히보기' 버튼 클릭시 /bookDetail/<int:book_id> 로 넘겨줌
        '''
        user_object = User.query.filter(User.email == session.get('user_email')).first()
        if user_object is None:
            flash('로그인 후 이용해주세요.')
            return render_template("signup.html")
        
        book_list = Book.query.all()
        book_id = request.form.get('book_id')

        if not book_id:
            flash('book_id는 필수 파라미터 입니다.')
            # return redirect(url_for('main.book_list'))
            return render_template("main.html", book_list=book_list)
        
        try:
            book_id = int(book_id)
        except ValueError:
            flash('book_id는 정수여야 합니다.')
            return redirect('main.book_list')
        
        book_object = Book.query.filter(Book.id == book_id).first()
        user_object = User.query.filter(User.email == session.get('user_email')).first()
        print(user_object)

        if not book_object:
            flash('대출하려는 책을 찾을 수 없습니다.')
            # return redirect(url_for('main.book_list'))
            return render_template('main.html', book_list=book_list)
        
        # 책의 재고가 0인 경우
        if book_object.remaining == 0:
            flash('재고가 없어서 대여할 수 없습니다. 다른 책을 대여해주세요.')
        
        # 이미 대여한 책인 경우
        rental_info_list = Rent.query.filter(
            (Rent.return_date == None) 
            & (Rent.rental_user_id == user_object.id)
        ).all()
        
        for book in rental_info_list:
            if book.id == book_id:
                flash('이미 대여한 책입니다. 마이페이지에서 확인해주세요.')
                return redirect('/mypage')
                # return render_template('mypage.html', rental_list=rental_list)
        
        book_object.remaining -= 1  # 재고(대여 가능으로 표시되는 수): -1
        book_object.rental_val += 1  # 총 대여 횟수: +1

        now = datetime.now()
        rental_date = now.strftime('%Y-%m-%d %H:%M:%S')
        # rental_date = datetime.now()

        
        rent_object = Rent(
            rental_date=rental_date,
            rental_user=user_object,
            book_id=book_id,
        )

        db.session.add(rent_object)
        db.session.commit()

        flash(f'{book_object.name}을 대여했습니다.')

        # return redirect(url_for('main.book_list'))
        return render_template("main.html", book_list=book_list)


book_list_view = BookListView.as_view('book_list')
bp.add_url_rule('/', view_func=book_list_view, methods=['GET', 'POST'])
