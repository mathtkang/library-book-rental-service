# [웹 서비스 프로젝트] 도서관 대출 서비스📚

---

### ⭐️프로젝트 소개

---

도서관에 있는 책을 온라인으로 관리할 수 있는 웹 서비스  
책의 상세 정보를 확인할 수 있는 페이지와 대여/반납 기능을 통해 도서 관리를 할 수 있는 웹 서비스 제작

### 👩‍💻주요 사용 기술

`Flask` `SQLAlchemy` `PyMySQL` `Flask-Login` `JQuery` `MySQL` `HTML` `Flask Jinja2`

### ✅구현 기능

---

**[로그인]**

- 아이디(이메일 형식)와 비밀번호([링크1](<https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/(%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%EC%9C%84%EC%9B%90%ED%9A%8C)%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98%EA%B8%B0%EC%88%A0%EC%A0%81%C2%B7%EA%B4%80%EB%A6%AC%EC%A0%81%EB%B3%B4%ED%98%B8%EC%A1%B0%EC%B9%98%EA%B8%B0%EC%A4%80/(2020-5,20200811)>), [링크2](https://www.kisa.or.kr/public/laws/laws3_View.jsp?cPage=7&mode=view&p_No=259&b_No=259&d_No=102&ST=T&SV=)에 맞는 최소 8자리 이상의 길이)를 입력 시 로그인 성공
- 로그인한 유저를 session으로 관리

**[회원가입]**

- 유저로부터 아이디(이메일), 비밀번호, 이름(한글, 영문) 정보를 입력받으면 회원가입 성공
- 비밀번호는 [링크1](<https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/(%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8%EC%9C%84%EC%9B%90%ED%9A%8C)%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%EC%9D%98%EA%B8%B0%EC%88%A0%EC%A0%81%C2%B7%EA%B4%80%EB%A6%AC%EC%A0%81%EB%B3%B4%ED%98%B8%EC%A1%B0%EC%B9%98%EA%B8%B0%EC%A4%80/(2020-5,20200811)>), [링크2](https://www.kisa.or.kr/public/laws/laws3_View.jsp?cPage=7&mode=view&p_No=259&b_No=259&d_No=102&ST=T&SV=)에 맞추어 영문, 숫자, 특수문자 중 2종류 이상을 조합해서 최소 10자리 이상 또는 3종류 이상을 조합하여 최소 8자리 이상의 길이로 구성
- 비밀번호 확인란을 통해서 2번의 입력값이 일치

**[로그아웃]**

- 로그인 해제 후 현재 session에서 제거

**[메인 페이지]**

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

**[책소개]**

- 메인 페이지의 책 이름 클릭시 접근 가능
- 책 소개 출력
- 가장 최신 날짜의 댓글부터 정렬 후 보이기
- 댓글 작성 및 평가 점수 기입 (필수입력)

**[대여기록]**

- 유저의 대여, 예약, 반납 등 모든 사항 출력

### Commit Message Template

---

```
################
# <type>(<scope>) : <subject>
# 제목은 50자 이내 / 변경사항이 "무엇"인지 명확히 작성 / 끝에 마침표 X
# 타입과 제목은 필수 / 범위는 선택
# 예) feat : 로그인 기능 추가

# 바로 아래 공백 유지 (제목과 본문의 분리를 위함)

################
# Body Message (선택사항)
# 본문(구체적인 내용)을 아랫줄에 작성
# 여러 줄의 메시지를 작성할 땐 "-"로 구분 (한 줄은 72자 이내)

################
# 꼬릿말(footer)을 아랫줄에 작성 (현재 커밋과 관련된 이슈 번호 추가 등)
# 예) Close #7

# Issue Tracker Number or URL

# --- COMMIT END ---
# <type> list
#   feat    : 새로운 기능
#   fix     : 버그
#   refactor: 코드 리팩토링
#   style   : 코드 의미에 영향을 주지 않는 변경사항 (형식 지정, 세미콜론 누락 등)
#   docs    : 문서의 추가, 수정, 삭제
#   test    : 테스트 추가, 수정, 삭제 (비즈니스 로직에 변경 없음)
#   chore   : 기타 변경사항 (빌드 부분 혹은 패키지 매니저 수정사항)
# ------------------
# Remember me ~
#   Capitalize the subject line
#     제목 첫 글자를 대문자로
#   Use the imperative mood in the subject line
#     제목은 명령문 사용 (과거형 X)
#   Do not end the subject line with a period
#     제목 끝에 마침표(.) 금지
#   Separate subject from body with a blank line
#     제목과 본문을 한 줄 띄워 분리하기 (빈 행으로 구분)
#   Use the body to explain what and why vs. how
#     본문은 "어떻게" 보다 "무엇을", "왜"를 설명한다.
#   Can use multiple lines with "-" for bullet points in body
#     본문에 여러줄의 메시지(목록)를 작성할 땐 "-"로 구분
# ------------------
```

### 🔗참고자료

---
