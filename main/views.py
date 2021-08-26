import traceback
from django.shortcuts import render, redirect
from django.views import View
from django.http import QueryDict
from django.http import HttpResponse
from .models import Member
from emailSend.views import send
from random import randint
import hashlib

# Create your views here.
def index(request):
    # try:
    #     # cookie 방식
    #     member_id = request.COOKIES['member_id']
    #     return render(request, 'main/index.html')
    # except Exception as e:
    #     print('e: ', str(e))
    #     return redirect('/signin/')

    # Session 방식
    if 'email' in request.session.keys():
        return render(request, 'main/index.html')
    return redirect('signin')


class SignUpView(View):
    def get(self, request):
        return render(request, 'main/signup.html')

    def post(self, request):
        """ 회원가입 기능 처리 """
        query_dict = QueryDict(request.body)
        username, email, pwd = query_dict['username'], query_dict['email'], query_dict['pwd']
        if username and email and pwd:
            try:
                sha256 = hashlib.sha256()
                sha256.update(pwd.encode('utf-8'))
                hashed_pwd = sha256.hexdigest()
                member = Member(name=username, email=email, pwd=hashed_pwd)
                if member:
                    member.save()
                    # Send email
                    verify_code = randint(1000, 9999)
                    is_send, msg = send(email, verify_code)
                    print(f'is_send: {is_send}, msg: {msg}')
                    if is_send:
                        response = redirect('verify')

                        # 1)쿠키 방식
                        # response.set_cookie('verify_code', verify_code)
                        # response.set_cookie('member_id', member.id)

                        # 2)세션방식
                        request.session['verify_code'] = verify_code
                        request.session['member_id'] = member.id
                        return response
                    else:
                        data = {'msg': '회원가입 메일 전송 실패! 이메일 인증번호 재요청이 필요합니다.'}
                        return redirect('signup', data)
            except Exception as e:
                print('e: ', str(e))
                data = {'msg': str(e)}
                traceback.print_exc()
                return redirect('signup', data)  # # 뷰별칭 으로 호출


class VerifyView(View):
    def get(self, request):
        return render(request, 'main/verify_code.html')

    def post(self, request):
        query_dict = QueryDict(request.body)
        # cookie_code = request.COOKIES.get('verify_code')
        # member_id = request.COOKIES.get('member_id')

        cookie_code = request.session['verify_code']
        member_id = request.session['member_id']
        if int(query_dict['verify_code']) == cookie_code:
            member = Member.objects.get(id=member_id)
            if member:
                member.is_verify = True
                member.save()
                response = redirect('index_page')
                # response.set_cookie('member_id', member.id)
                # response.delete_cookie('verify_code')

                del request.session['verify_code']
                del request.session['member_id']
                request.session['email'] = member.email
                request.session['name'] = member.name
                return response
            else:
                return HttpResponse('회원 정보를 찾을 수 없습니다.' + member_id)
        return HttpResponse('인증번호가 일치하지 않습니다. verify_code: ' + query_dict['verify_code'])


class SignInView(View):
    def get(self, request):
        return render(request, 'main/signin.html')

    def post(self, request):
        query_dict = QueryDict(request.body)
        member_set = Member.objects.filter(email=query_dict['email'])
        # print(member_set)
        if member_set:
            member = member_set[0]
            if member.is_verify is False:
                # data = {'msg': '이메일 인증을 완료해주세요'}
                return redirect('/signin/')

            raw = query_dict['pwd']
            sha256 = hashlib.sha256()
            sha256.update(raw.encode('utf-8'))
            pwd = sha256.hexdigest()
            if member.pwd == pwd:
                response = redirect('index_page')
                # response.set_cookie('member_id', member.id)

                request.session['email'] = member.email
                request.session['name'] = member.name
                return response
            else:
                # {'msg': '암호를 확인하세요'}
                return redirect('/signin/')  # 경로 호출
        else:
            #  {'msg': '회원 정보가 존재하지 않습니다.'}
            return redirect('/signin/')


class LogOutView(View):
    def get(self, request):
        del request.session['email']
        del request.session['name']
        return redirect('signin')

        # response = redirect('signin')  # 뷰별칭 으로 호출
        # response.delete_cookie('member_id')
        # return response

    def post(self, request):
        pass
