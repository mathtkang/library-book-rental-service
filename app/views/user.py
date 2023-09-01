from datetime import datetime
from flask import redirect, request, render_template, flash, url_for
from flask import Blueprint, session
from flask.views import MethodView

from app.models import User, Book, Rent, Review
from app import db


bp = Blueprint('user', __name__, url_prefix='/')

class MyPageView(MethodView):
    def get(self):
        '''
        Redirect page: mypage.html
        대여 기록 반환
        '''
        user_email = session.get('user_email')
        if user_email:
            user_object = User.query.filter(User.email == user_email).first()
            rental_list = Rent.query.filter(
                Rent.rental_user == user_object
            ).order_by(
                Rent.return_date.is_(None).desc(),  # return_date가 None인 것부터 내림차순 정렬
                Rent.rental_date.desc()  # rental_date가 최신인 것부터 내림차순 정렬
            ).all()
            return render_template('mypage.html', rental_list=rental_list)
        else:
            flash('로그인 후 이용해주세요.')
            return redirect(url_for('auth.login'))

    def post(self):
        '''
        반납하기 기능
        '반납하기' 버튼 클릭시 대여목록에서 지우고, 책 반납하기
        '''
        user_object = User.query.filter(User.email == session['user_email']).first()
        rental_list = Rent.query.filter(Rent.rental_user == user_object).all()

        rented_book_id = int(request.form['book_id'])
        rental_book_object = Rent.query.filter_by(id=rented_book_id).first()

        if not rental_book_object:
            flash('대여 정보를 찾을 수 없습니다.')
        else:
            book_object = rental_book_object.book
            book_object.remaining += 1

            if rental_book_object.return_date is None:
                rental_book_object.return_date = datetime.now()

                past_rental_records = Rent.query.filter(
                    Rent.book_id == book_object.id,
                    Rent.rental_user_id == user_object.id,
                    Rent.return_date.isnot(None)
                ).all()

            db.session.commit()
            flash('반납했습니다.')

        return render_template('mypage.html', rental_list=rental_list)


bp.add_url_rule('/mypage', view_func=MyPageView.as_view('mypage'), methods=['GET', 'POST'])
