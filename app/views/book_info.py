from datetime import datetime
from flask import redirect, request, render_template, flash
from flask import Blueprint, session
from flask.views import MethodView

from app import db
from app.models import User, Book, Rent, Review


bp = Blueprint('book_info', __name__, url_prefix='/')

# @bp.route('/bookDetail/<int:book_id>', methods=['GET', 'POST'])
class BookDetailView(MethodView):
    def get(self, book_id):
        '''
        Redirect page: book_detail.html
        책 상세 페이지 반환
        TODO: book_detail.html 페이지에 대여하기 버튼 구현
        '''
        book_object = Book.query.filter(Book.id == book_id).first()

        if book_object is None:
            flash('해당 id에 대한 책을 찾을 수 없습니다.')
            return redirect('/')

        # 지금까지 작성된 댓글을 최신순(DESC)으로 가져온다
        review_list = Review.query.filter(
            Review.book_id == book_id
        ).order_by(Review.write_time.desc()).all()

        return render_template('book_detail.html', book_detail=book_object, review_list=review_list)

    def post(self, book_id):
        '''
        댓글 작성 기능
        Redirect page: main.html의 '자세히보기'로 넘어옴
        '''
        content = request.form['review']
        rating = int(request.form['rating'])
        now = datetime.now()
        write_time = now.strftime('%Y-%m-%d %H:%M:%S')

        # 댓글 내용과 별점이 없는 경우
        if not content:
            flash('댓글 내용을 작성해주세요.')
            return redirect(f'/bookDetail/{book_id}')
        if not rating:
            flash('별점을 선택해주세요.')
            return redirect(f'/bookDetail/{book_id}')

        user_object = User.query.filter(User.email == session.get('user_email')).first()

        # 댓글 작성이 올바르게 된 경우 : db에 추가
        review_object = Review(
            content=content,
            rating=rating,
            write_time=write_time,
            written_user_id=user_object.id,
            book_id=book_id,
        )

        db.session.add(review_object)

        # 평점 작성에 맞춰서 평점 평균 구하기
        book_object = Book.query.filter(Book.id == book_id).first()
        review_list = Review.query.filter(Review.book_id == book_id).all()
        rating_sum = 0

        for review in review_list:
            rating_sum += review.rating
        book_rating = int(rating_sum / len(review_list))
        book_object.star = book_rating

        db.session.commit()

        return redirect(f'/bookDetail/{book_id}')


# @bp.route('/bookDetail/<int:book_id>/<int:review_id>', methods=['PUT', 'DELETE'])
# class ReviewEditView(MethodView):
#     def put(self, book_id, comment_id):
#         '''
#         TODO: 댓글 수정 기능
#         '''
#         new_content = request.form['review']
#         review = Review.query.get(comment_id)

#         if review is None:
#             flash('해당 댓글을 찾을 수 없습니다.')
#         elif review.user_email != session['user_email']:
#             flash('본인의 댓글만 수정할 수 있습니다.')
#         else:
#             review.content = new_content
#             db.session.commit()
        
#         return redirect(f'/bookDetail/{book_id}')

#     def delete(self, book_id, comment_id):

#         '''
#         TODO: 댓글 삭제 기능
#         '''
#         review = Review.query.get(comment_id)

#         if review is None:
#             flash('해당 댓글을 찾을 수 없습니다.')
#         elif review.user_email != session['user_email']:
#             flash('본인의 댓글만 삭제할 수 있습니다.')
#         else:
#             db.session.delete(review)
#             db.session.commit()
        
#         return redirect(f'/bookDetail/{book_id}')


book_detail_view = BookDetailView.as_view('book_info')
bp.add_url_rule('/bookDetail/<int:book_id>', view_func=book_detail_view, methods=['GET', 'POST'])
