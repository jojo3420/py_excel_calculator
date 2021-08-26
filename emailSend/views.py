import traceback

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# Create your views here.

def send_page(request):
    is_send, msg = send('jjjhhhvvv@naver.com', 1234)
    if is_send:
        return HttpResponse('메일 전송 성공')
    return HttpResponse('메일 전송 실패: ' + msg)


def read_email_info(file_path):
    with open(file_path) as stream:
        from_email, pwd = stream.readlines()
        return from_email.strip(), pwd.strip()


def send(to_email, verify_code):
    """
    이메일 전송하기 (gmail smtp)
    :param to_email: 받는 이메일주소
    :param verify_code: 인증번호코드 4자리
    :return:
    """
    try:
        html_str = render_to_string('emailSend/email_format.html', {'verify_code': verify_code})
        subject = '회원가입을 환영합니다.'
        from_email, _pwd = read_email_info('.env')
        email_message = EmailMessage(subject=subject, body=html_str, from_email=from_email, bcc=[to_email])
        email_message.content_subtype = 'html'
        email_message.send()
        return True, ''
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return False, str(e)
