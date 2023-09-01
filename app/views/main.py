from datetime import datetime
from flask import redirect, request, render_template, flash, url_for, jsonify
from flask import Blueprint, session
from flask.views import MethodView

from app.models import User, Book, Rent, Review
from app import db

bp = Blueprint('main', __name__, url_prefix='/')


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
        - TODO: 대여횟수 늘어나는 부분 수정 필요!
        '''
        book_id = request.form.get('book_id')
        user_object = User.query.filter(User.email == session.get('user_email')).first()

        if user_object is None:
            flash('로그인 또는 회원가입 이후 이용해주세요.')
            return redirect(url_for('auth.login'))
        
        book_list = Book.query.all()

        if not book_id:
            flash('book_id는 필수 파라미터 입니다.')
            return redirect(url_for('main.book_list'))
        try:
            book_id = int(book_id)
        except ValueError:
            flash('book_id는 정수여야 합니다.')
            return redirect(url_for('main.book_list'))
        
        book_object = Book.query.filter(Book.id == book_id).first()

        if not book_object:
            flash('대출하려는 책을 찾을 수 없습니다.')
            return redirect(url_for('main.book_list'))
        
        # 책의 재고가 0인 경우
        if book_object.remaining == 0:
            flash('재고가 없어서 대여할 수 없습니다. 다른 책을 대여해주세요.')
            return redirect(url_for('main.book_list'))
        
        # 이미 대여한 책인 경우
        rental_info = Rent.query.filter(
            (Rent.rental_user == user_object)
            & (Rent.book_id == book_id)
            & (Rent.rental_date != None) 
        ).first()
        
        if rental_info:
            flash('이미 대여한 책입니다. 마이페이지에서 확인해주세요.')
            return redirect('/mypage')
        
        book_object.remaining -= 1  # 재고(대여 가능으로 표시되는 수): -1

        rental_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        rent_object = Rent(
            rental_date=rental_date,
            rental_user=user_object,
            book_id=book_id,
            rental_num=1,
        )
        # rent_object.rental_num += 1  # 총 대여 횟수: +1

        db.session.add(rent_object)
        db.session.commit()

        flash(f'{book_object.name}을 대여했습니다.')

        return render_template("main.html", book_list=book_list)


class SearchBookView(MethodView):
    def get(self):
        search_query = request.args.get('search_book_name')

        search_results = []

        if search_query:
            search_query = search_query.lower()  # 소문자 변환
            search_results = Book.query.filter(Book.name.ilike(f'%{search_query}%')).all()

        return render_template("search_list.html", search_results=search_results)


bp.add_url_rule('/main', view_func=BookListView.as_view('book_list'), methods=['GET', 'POST'])
bp.add_url_rule('/search', view_func=SearchBookView.as_view('search_book'), methods=['GET'])