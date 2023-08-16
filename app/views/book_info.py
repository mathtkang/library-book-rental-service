from datetime import datetime
from flask import redirect, request, render_template, flash, jsonify
from flask import Blueprint, session
from flask.views import MethodView

from app import db
from app.models import User, Book, Rent, Review


bp = Blueprint('book_info', __name__, url_prefix='/')

class BookDetailView(MethodView):
    def get(self, book_id):
        '''
        Redirect page: book_detail.html
        ✅ 책 상세 페이지 반환
        - TODO: book_detail.html 페이지에 대여하기 버튼 구현
        '''
        book_object = Book.query.filter(Book.id == book_id).first()

        if book_object is None:
            flash('해당 id에 대한 책을 찾을 수 없습니다.')
            return redirect('/')

        # 지금까지 작성된 댓글을 최신순(DESC)으로 가져온다
        review_list = Review.query.filter(
            Review.book_id == book_id
        ).order_by(Review.created_at.desc()).all()

        return render_template('book_detail.html', book_detail=book_object, review_list=review_list)

    def post(self, book_id):
        '''
        ✅ Redirect page: main.html의 '자세히보기'로 넘어옴
        ✅ 댓글 작성 기능
        '''
        content = request.form['review']
        rating = int(request.form['rating'])
        now = datetime.now()
        created_at = now.strftime('%Y-%m-%d %H:%M:%S')

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
            created_at=created_at,
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


class ReviewEditView(MethodView):
    def post(self, book_id, review_id):
        '''
        ✅ 댓글 수정 기능
        '''
        updated_content = request.form['updated_review']
        written_review_object = Review.query.filter(Review.id == review_id).first()

        if written_review_object is None:
            flash('해당 댓글을 찾을 수 없습니다.')
        elif written_review_object.written_user.email != session['user_email']:
            flash('본인의 댓글만 수정할 수 있습니다.')
        else:
            written_review_object.content = updated_content
            written_review_object.updated_at = datetime.utcnow()  # 현재 시간으로 업데이트
            db.session.commit()
        
        return redirect(f'/bookDetail/{book_id}')

    def delete(self, book_id, review_id):
        '''
        ✅ 댓글 삭제 기능
        '''
        review = Review.query.get(review_id)

        if review is None:
            flash('해당 댓글을 찾을 수 없습니다.')
            return jsonify({
                'success': False, 
                'message': '해당 댓글을 찾을 수 없습니다.'
            })
        elif review.written_user.email != session['user_email']:
            flash('본인의 댓글만 삭제할 수 있습니다.')
            return jsonify({
                'success': False, 
                'message': '본인의 댓글만 삭제할 수 있습니다.'
            })
        else:
            db.session.delete(review)
            db.session.commit()
            
        return jsonify({
            'success': True, 
            'message': '댓글이 삭제되었습니다.'
        })


bp.add_url_rule('/bookDetail/<int:book_id>', view_func=BookDetailView.as_view('book_info'), methods=['GET', 'POST'])
bp.add_url_rule('/bookDetail/<int:book_id>/<int:review_id>', view_func=ReviewEditView.as_view('review_edit'), methods=['POST', 'DELETE'])