<h1>주의 사항</h1>

SMTP(간편 전자 메일 발송 프로토콜)을 사용해서 회원가입 기능 중 이메일발송을 구현할려면 다음과 같이 해야함..<br>
fourthproject/settings.py에서 밑에 보면<br> 
EMAIL_HOST_USER를 자신의 'GOOGLE메일주소'입력하고<br>
EMAIL_HOST_PASSWORD를 'GOOGLE메일 비밀번호'로 하고<br>
SERVER_EMAIL을 EMAIL_HOST_USER로 정하고<br>
DEFAULT_FROM_MAIL = '구글메일주소에서 @GMAIL.COM빼기'
EX. 'ensk960405'<br>
이제 회원들에게 발송할 서버 이메일이 정해졌다(자신의 지메일)
<br>
그리고 이제 gmail server를 통해 smtp를 활용하기 위해 두 가지만 더하면 된다...
1. https://support.google.com/mail/answer/7126229?hl=ko
에서 1단계 그대로 따라한 후<br>
2.구글에서 settings.py에 입력할 이메일로 로그인을 한후 
google 계정 칸을 눌러 왼쪽에 보안칸을 누른 뒤
중간에 보안 수준 액세스 버튼이 있는데 <br>
밑의 액세스 버튼을 눌러서 보안 수준이 낮은 앱을 허용칸을 눌러야한다.<br>
그러고 회원가입을 하면 이메일 인증, 비밀번호 찾기를 할때 이메일 인증이 가능!<br><br><br>
저번 만남 때 슈퍼유저를 만들려고 했지만 TypeError: create_superuser() missing 1 required positional argument: 'username'라는 오류가 떠서 확인해보니<br>
User 모델을 커스터마이징해서 email이 아이디값을 갖게 하려고 하다보니 필요없는 건 주석처리를 했는데 <br>
알고보니 REQUIRED_FIELDS뜻이 createsuperuser커맨드로 유저를 생성할 때 나타날 필드 목록이였다.
없어도 상관없을 것 같은데 내가 먼저 처음에 주석 달기 전에 슈퍼유저를 만든 적이 있어서 오류가 난 것 같다.


