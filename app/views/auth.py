from flask import redirect, request, render_template, jsonify, Blueprint, session, g, url_for, flash
from app.models import User, Book, Rent, Review
from flask_bcrypt import Bcrypt
from app import db

from flask_login import login_required, login_user, current_user, logout_user
from email_validator import validate_email, EmailNotValidError
# from werkzeug.security import generate_password_hash, check_password_hash   #Bcrypt에 포함되어있음

bp = Blueprint('user', __name__, url_prefix='/')
bcrypt = Bcrypt()


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    Redirect page: signup.html
    1. GET : 회원가입
    2. POST : user db와 비교해서 새로운 유저 생성
    '''
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        password = request.form['password']
        password2 = request.form['password2']

        # front에서도 구현 가능
        if not user_name:
            flash('이름을 입력해주세요.')
            return render_template('signup.html')
        if not user_email:
            flash('아이디를 입력해주세요.')
            return render_template('signup.html')
        else:
            try:
                validate_email(user_email)
            except EmailNotValidError:
                flash('이메일 형식이 아닙니다.')
                return render_template('signup.html')
        if not password or not password2:
            flash('비밀번호를 입력해주세요.')
            return render_template('signup.html')
        if password != password2:
            flash('비밀번호가 일치하지 않습니다.')
            return render_template('signup.html')
        if len(password) < 8:
            flash("비밀번호는 8자리 이상입니다.")
            return render_template('signup.html')
        if not any(char.isdigit() for char in password):
            flash('숫자가 포함되어야합니다.')
            return render_template('signup.html')
        special_char = '`~!@#$%^&*()_+|\\}{[]":;\'?><,./'
        if not any(char in special_char for char in password):
            flash('특수문자가 포함되어야합니다.')
            return render_template('signup.html')

        # 비밀번호 암호화
        pw_hash = bcrypt.generate_password_hash(password)

        # 사용자 중복 확인
        user_check = User.query.filter(
            User.user_email == user_email).first()
        if user_check:
            flash("이미 존재하는 이메일입니다.")
            return render_template('signup.html')
            # return jsonify(result='email_check')

        # db에 유저 생성
        user_data = User(user_name=user_name,
                                user_email=user_email, password=pw_hash)
        db.session.add(user_data)
        db.session.commit()

        flash("회원가입이 완료되었습니다. 로그인해주세요!😊")
        return redirect("/login")

    # get방식인 경우
    return render_template('signup.html')


@bp.route('/login', methods=["GET", "POST"])
def login():
    '''
    보여지는 화면 : login.html
    1. GET : 로그인
    2. POST : user db와 비교해서 로그인 성공
    권한 검사 아직 X : 세션에 유저 이메일 값이 없는 경우에만 실행하도록
    구현하고 싶은 부분 : 체크박스 클릭시 다음번 로그인시 세션 유지
    '''
    if request.method == 'POST':
        user_email = request.form['user_email']
        password = request.form['password']

        # front에서도 구현 가능
        if not user_email:
            flash('아이디를 입력해주세요.')
            return render_template('login.html')
        else:
            try:
                validate_email(user_email)
            except EmailNotValidError:
                flash('이메일 형식이 아닙니다.')
                return render_template('login.html')
        if not password:
            flash('비밀번호를 입력해주세요.')
            return render_template('login.html')

        # 사용자 db가져오기
        user_data = User.query.filter(
            User.user_email == user_email).first()

        # 사용자 존재하는 경우
        if user_data is not None:
            # 암호화된 비밀번호 일치 여부
            if bcrypt.check_password_hash(user_data.password, password):
                # 세션 생성
                session.clear()
                session['user_name'] = user_data.user_name
                session['user_email'] = user_data.user_email

                flash("로그인 되었습니다!")  # 안나옴
                return redirect("/")
                # return jsonify(result='success')

            # 비밀번호 일치하지 않음
            else:
                flash("비밀번호를 다시 확인해주세요.")
                return render_template('login.html')
                # return jsonify({"result": "fail"})

        # 사용자 없음
        else:
            flash("해당 아이디가 없습니다. 회원가입해주세요.")
            return redirect("/signup")
            # return jsonify({"result": "user_none"})
    else:  # GET
        return render_template('login.html')


@bp.route('/logout')
def logout():
    '''
    로그아웃
    세션에서 사용자 정보 지워준다.
    '''
    session.clear()
    flash("로그아웃 되었습니다.")
    return redirect("/")
