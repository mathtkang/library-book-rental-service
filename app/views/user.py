from datetime import datetime
from flask import redirect, request, render_template, flash, url_for
from flask import Blueprint, session
from flask.views import MethodView

from app.models import User, Book, Rent, Review
from app import db


bp = Blueprint('user', __name__, url_prefix='/')

# @bp.route("/mypage", methods=['GET', 'POST'])
class MyPageView(MethodView):
    def get(self):
        '''
        Redirect page: mypage.html
        대여 기록 반환
        '''
        user_object = User.query.filter(User.email == session['user_email']).first()

        rental_list = Rent.query.filter(
            Rent.rental_user_id == user_object.id
        ).all()
        return render_template('mypage.html', rental_list=rental_list)

    def post(self):
        '''
        반납하기 기능
        '반납하기' 버튼 클릭시 대여목록에서 지우고, 책 반납하기
        '''
        user_object = User.query.filter(User.email == session['user_email']).first()
        rental_list = Rent.query.filter(
            Rent.rental_user_id == user_object.id
        ).all()

        rented_book_id = request.form['book_id']
        if not rented_book_id:
            flash('존재하지 않는 대여입니다.')
            return render_template('mypage.html', rental_list=rental_list)

        try:
            rented_book_id = int(rented_book_id)
        except ValueError:
            flash('올바르지 않은 대여번호입니다.')
            return render_template('mypage.html', rental_list=rental_list)

        book_object = Book.query.filter(Book.id == rented_book_id).first()
        if not book_object:
            flash('책 정보를 찾을 수 없습니다.')
            return render_template('mypage.html', rental_list=rental_list)
        
        rental_book_object = Rent.query.filter(
            (Rent.id == rented_book_id)
            & (Rent.rental_user_id == user_object.id)
        ).first()

        if not rental_book_object:
            flash('대여 정보를 찾을 수 없습니다.')
        
        book_object.remaining += 1  # 재고: +1

        now = datetime.now()
        rental_book_object.return_date = now.strftime('%Y-%m-%d %H:%M:%S')

        db.session.delete(rental_book_object)
        db.session.commit()

        flash('반납했습니다.')

        return redirect('/mypage')



mypage_view = MyPageView.as_view('mypage')
bp.add_url_rule('/mypage', view_func=mypage_view, methods=['GET', 'POST'])
