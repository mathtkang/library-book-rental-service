from flask import redirect, request, render_template, flash
from flask import Blueprint, session
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from email_validator import validate_email, EmailNotValidError

from app import db
from app.models import User


bp = Blueprint('auth', __name__, url_prefix='/')
bcrypt = Bcrypt()


class SignupView(MethodView):
    def get(self):
        '''
        Redirect page: signup.html
        '''
        return render_template('signup.html')

    def post(self):
        '''
        회원가입 기능
        '''
        name = request.form['user_name']
        email = request.form['user_email']
        password = request.form['password']
        password2 = request.form['password2']
        
        if not name or not email or not password or not password2:
            flash('모든 필드(이름, 이메일, 비밀번호)를 입력해주세요.')
            return render_template('signup.html')

        try:
            validate_email(email)
        except EmailNotValidError:
            flash('이메일 형식이 아닙니다.')
            return render_template('signup.html')
        
        if password != password2:
            flash('비밀번호가 일치하지 않습니다.')
            return render_template('signup.html')
        
        if len(password) < 8:
            flash("비밀번호는 8자리 이상입니다.")
            return render_template('signup.html')
        
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            flash('비밀번호는 숫자와 문자를 혼합하여야 합니다.')
            return render_template('signup.html')
        
        special_char = '`~!@#$%^&*()_+|\\}{[]":;\'?><,./'
        if not any(char in special_char for char in password):
            flash('특수문자가 포함되어야 합니다.')
            return render_template('signup.html')
        
        # 이메일 중복 확인
        existing_user = User.query.filter(User.email == email).first()
        if existing_user:
            flash("이미 존재하는 이메일입니다.")
            return render_template('signup.html')


        # 비밀번호 암호화
        hashed_password = bcrypt.generate_password_hash(password)

        # db에 유저 생성
        user_object = User(
            name=name,
            email=email,
            password=hashed_password
        )
        db.session.add(user_object)
        db.session.commit()

        flash("회원가입이 완료되었습니다. 로그인해주세요!😊")

        return redirect("/login")


class LoginView(MethodView):
    def get(self):
        '''
        Redirect page: login.html
        '''
        return render_template('login.html')

    def post(self):
        '''
        로그인 기능
        TODO: 자동로그인(체크박스 클릭시) 세션 유지
        (권한 검사의 필요성?)
        '''
        email = request.form['user_email']
        password = request.form['password']

        if not email:
            flash('이메일를 입력해주세요.')
            return render_template('login.html')
        
        try:
            validate_email(email)
        except EmailNotValidError:
            flash('이메일 형식이 아닙니다.')
            return render_template('login.html')
        
        if not password:
            flash('비밀번호를 입력해주세요.')
            return render_template('login.html')

        user_object = User.query.filter(email==email).first()
        if user_object is None:
            flash("해당 이메일이 없습니다. 회원가입해주세요.")
            return redirect("/signup")
        
        # 비밀번호 검증
        if bcrypt.check_password_hash(user_object.password, password):
            session.clear()
            session['user_name'] = user_object.name
            session['user_email'] = user_object.email

            flash("로그인 되었습니다!")
            return redirect("/")
        else:
            flash("비밀번호를 다시 확인해주세요.")
            return render_template('login.html')


class LogoutView(MethodView):
    def get(self):
        '''
        세션에서 사용자 정보 지워줌
        '''
        session.clear()
        flash("로그아웃 되었습니다.")
        return redirect("/")
    


signup_view = SignupView.as_view('signup')
bp.add_url_rule('/signup', view_func=signup_view, methods=['GET', 'POST'])

login_view = LoginView.as_view('login')
bp.add_url_rule('/login', view_func=login_view, methods=['GET', 'POST'])

logout_view = LogoutView.as_view('logout')
bp.add_url_rule('/logout', view_func=logout_view, methods=['GET'])
