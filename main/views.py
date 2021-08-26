import traceback
from django.shortcuts import render, redirect
from django.views import View
from django.http import QueryDict
from django.http import HttpResponse
from .models import Member
from emailSend.views import send
from random import randint


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


class VerifyView(View):
    def get(self, request):
        return render(request, 'main/verify_code.html')

    def post(self, request):
        query_dict = QueryDict(request.body)
        cookie_code = request.COOKIES.get('verify_code')
        member_id = request.COOKIES.get('member_id')
        if query_dict['verify_code'] == cookie_code:
            member = Member.objects.get(id=member_id)
            if member:
                member.is_verify = True
                member.save()
                response = redirect('index_page')
                response.set_cookie('member', member)
                response.delete_cookie('verify_code')
                response.delete_cookie('user_id')
                return response
            else:
                return HttpResponse('회원 정보를 찾을 수 없습니다.' + member_id)
        return HttpResponse('인증번호가 일치하지 않습니다. verify_code: ' + query_dict['verify_code'])


class SignInView(View):
    def get(self, request):
        return render(request, 'main/signin.html')

    def post(self, request):
        pass


class SignUpView(View):
    def get(self, request):
        return render(request, 'main/signup.html')

    def post(self, request):
        """ 회원가입 기능 처리 """
        query_dict = QueryDict(request.body)
        username, email, pwd = query_dict['username'], query_dict['email'], query_dict['pwd']
        if username and email and pwd:
            try:
                member = Member(name=username, email=email, pwd=pwd)
                if member:
                    member.save()
                    # Send email
                    verify_code = randint(1000, 9999)
                    is_send, msg = send(email, verify_code)
                    print(f'is_send: {is_send}, msg: {msg}')
                    if is_send:
                        response = redirect('verify')
                        response.set_cookie('verify_code', verify_code)
                        response.set_cookie('member_id', member.id)
                        return response
                    else:
                        data = {'msg': '회원가입 메일 전송 실패! 이메일 인증번호 재요청이 필요합니다.'}
                        return redirect('signup', data)
            except Exception as e:
                print(str(e))
                data = {'msg': str(e)}
                traceback.print_exc()
                return redirect('signup', data)


class LoginOutView(View):
    def get(self, request):
        return redirect('signin')

    def post(self, request):
        pass
