# 도서관 대출 서비스 📚

## 📃 프로젝트 개요

- 도서관에 있는 책을 온라인으로 관리할 수 있는 웹 서비스
- 책의 상세 정보를 확인할 수 있는 페이지와 **대여/반납 기능**을 통해 도서 관리를 할 수 있는 웹 서비스입니다.
- 책의 상세 페이지에서 **별점 및 댓글을 작성**할 수 있고 수정/삭제가 가능합니다.


## 🛠 사용 기술

**Backend**
- ![python badge](https://img.shields.io/badge/Python-3776AB?&logo=Python&logoColor=white)
- ![flask badge](https://img.shields.io/badge/Flask-52BBE6?&logo=Flask&logoColor=white)
- ![sqlalchemy badge](https://img.shields.io/badge/SQLAlchemy-0C0C0E?&logo=Alchemy&logoColor=white)
- ![pyjwt badge](https://img.shields.io/badge/PyJWT-000000?&logo=jsonwebtokens&logoColor=white)

**Database**
- ![mysql badge](https://img.shields.io/badge/MySQL-4479A1?&logo=MySQL&logoColor=white)

**Front**
- ![jquery badge](https://img.shields.io/badge/JQuery-0769AD?&logo=JQuery&logoColor=white)
- ![jinja2 badge](https://img.shields.io/badge/Jinja2-B41717?&logo=Jinja&logoColor=white)

**Deploy**
- ![nginx badge](https://img.shields.io/badge/nginx-009639?&logo=nginx&logoColor=white)
- ![gunicorn badge](https://img.shields.io/badge/gunicorn-499848?&logo=gunicorn&logoColor=white)
- ![docker badge](https://img.shields.io/badge/Docker-2496ED.svg?style=flate&logo=Docker&logoColor=white)


**Environment**
- ![Visual Studio Code badge](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC.svg?style=flat&logo=Visual-Studio-Code&logoColor=white)
- ![postman badge](https://img.shields.io/badge/postman-FF6C37?style=flat&logo=Postman&logoColor=white)
- ![github badge](https://img.shields.io/badge/GitHub-181717.svg?style=flat&logo=GitHub&logoColor=white)



## 📋 E-R Diagram
<img width="1000" alt="ERD" src="https://user-images.githubusercontent.com/51039577/259807080-54ea1196-ae60-4b11-96f0-885217eeb288.png">


## 📋 API 명세서 (request/response 포함)
[API 명세서 링크]()


## 🚀 AWS EC2 서비스 배포 주소
[도서관 서비스 주소]()


## 🕸 시스템 아키텍처
<img width="1000" alt="system structure" src="">


## 🔗 구현한 서비스의 동작을 촬영한 데모 영상 링크
[데모 영상 링크]()


## ✅ 구현 기능 설명

**[회원가입]**

- 유저로부터 아이디(이메일), 비밀번호, 이름(한글, 영문) 정보를 입력받으면 회원가입 성공
- 비밀번호는 [링크](<https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/(%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%EC%9C%84%EC%9B%90%ED%9A%8C)%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98%EA%B8%B0%EC%88%A0%EC%A0%81%C2%B7%EA%B4%80%EB%A6%AC%EC%A0%81%EB%B3%B4%ED%98%B8%EC%A1%B0%EC%B9%98%EA%B8%B0%EC%A4%80/(2020-5,20200811)>)에 맞추어 영문, 숫자, 특수문자 중 2종류 이상을 조합해서 최소 10자리 이상 또는 3종류 이상을 조합하여 최소 8자리 이상의 길이로 구성
- 비밀번호 확인란을 통해서 2번의 입력값이 일치

**[로그인]**

- 아이디(이메일 형식)와 비밀번호([링크](<https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/(%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%EC%9C%84%EC%9B%90%ED%9A%8C)%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98%EA%B8%B0%EC%88%A0%EC%A0%81%C2%B7%EA%B4%80%EB%A6%AC%EC%A0%81%EB%B3%B4%ED%98%B8%EC%A1%B0%EC%B9%98%EA%B8%B0%EC%A4%80/(2020-5,20200811)>)에 맞는 최소 8자리 이상의 길이)를 입력 시 로그인 성공
- 로그인한 유저를 session으로 관리

**[로그아웃]**

- 로그인 해제 후 현재 session에서 제거

**[메인페이지]**

- 현재 DB에 존재하는 모든 책 정보 가져오기 (제목, 출판사, 작가, 출판일, 총 페이지수, 국제 표준 도서 번호, 사진, 제목, 평점, 남은 권수 등)
- 책 이름 클릭 시 책 소개 페이지로 이동
- 책의 평균(현재 DB 상에 담겨있는 모든 평점의 평균)은 숫자 한자리수로 반올림해서 표기
- 페이지네이션 기능 추가 (한 페이지 당 8권의 책만을 표기)

**[대여하기]**

- 메인 페이지의 '대여하기' 버튼 클릭시 실행
- 현재 DB 상에 책이 존재하는 경우, 책을 대여하고 책 권수를 -1, 존재하지 않는 경우, 대여가 불가능하다는 메시지 반환
- 유저가 이미 책을 대여한 경우, 안내 메시지 반환

**[반납하기]**

- 유저가 대여한 책을 모두 출력
- '반납하기' 버튼 클릭 시 책 반납 (DB 상 책 권수 +1)

**[책 소개]**

- 메인 페이지의 책 이름 클릭시 접근 가능
- 책 소개 출력
- 가장 최신 날짜의 댓글부터 정렬 후 보이기
- 댓글 작성 및 평가 점수 기입 (필수입력)

**[별점 및 댓글 기능]**

- 책 소개 페이지에서 해당 책에 대한 별점과 댓글을 작성할 수 있음
- 별점은 1~5의 점수로 줄 수 있고, 댓글은 작성자만 수정/삭제 가능하도록 구현

**[대여 기록]**

- 마이페이지에서 유저의 대여, 예약, 반납 등 모든 사항 출력