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

        # 이름 중복 확인
        existing_user = User.query.filter(User.name == name).first()
        if existing_user:
            flash("이미 존재하는 이름입니다.")
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
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # db에 유저 생성
        user_object = User(
            name=name,
            email=email,
            password=hashed_password
        )
        
        db.session.add(user_object)
        db.session.commit()

        # return {"message": "User created successfully"}, 201

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

        user_object = User.query.filter(User.email == email).first()

        if user_object is None:
            flash("해당 이메일이 없습니다. 회원가입해주세요.")
            return render_template('signup.html')

        password = password.encode('utf-8')
        user_object.password = user_object.password.encode('utf-8')
        
        # 비밀번호 검증
        if not bcrypt.check_password_hash(user_object.password, password):
            print("here")
            flash("비밀번호를 다시 확인해주세요.")
            return render_template('login.html')

        session.clear()
        session['user_email'] = user_object.email
        session['user_name'] = user_object.name

        # 자동로그인 체크박스 확인
        if request.form.get('check2') == '2':
            session.permanent = True  # 세션의 활성화: 브라우저를 닫아도 세션이 지속되기 때문에 로그인 상태 유지 가능 (PERMANENT_SESSION_LIFETIME에 의존함)
        else:
            session.permanent = False  # PERMANENT_SESSION_LIFETIME 와는 무관하게 동작: 브라우저 닫으면 자동으로 세션 삭제
            session.modified = True  # 세션 변경사항을 Flask에 알려줌

        flash("로그인 되었습니다!😊")
        return redirect("/main")


class LogoutView(MethodView):
    def get(self):
        '''
        세션에서 사용자 정보 지워줌
        '''
        session.clear()  # 세션의 모든 데이터 삭제
        flash("로그아웃 되었습니다.")
        return redirect("/main")
    

bp.add_url_rule('/signup', view_func=SignupView.as_view('signup'), methods=['GET', 'POST'])
bp.add_url_rule('/login', view_func=LoginView.as_view('login'), methods=['GET', 'POST'])
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'), methods=['GET'])
