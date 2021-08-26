from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


class VerifyView(View):
    def get(self, request):
        return render(request, 'main/verify_code.html')

    def post(self, request):
        pass


class SignInView(View):
    def get(self, request):
        return render(request, 'main/signin.html')

    def post(self, request):
        pass


class SignUpView(View):
    def get(self, request):
        return render(request, 'main/signup.html')

    def post(self, request):
        pass


class LoginOutView(View):
    def get(self, request):
        return redirect('signin')

    def post(self, request):
        pass
