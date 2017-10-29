from django.contrib.auth import (
    get_user_model,
    logout as django_logout,
    login as django_login,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from config import settings
from member.forms import SignupForm, LoginForm

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        # SignupForm에 바인딩된 request.POST
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # 회원가입이 완료되면 로그인해주고 인덱스 화면으로
            django_login(request, user)
            return redirect('post:post_list')
    # GET요청시  비어있는 SignupForm을 전달
    return render(
        request,
        'member/signup.html',
        {
            'signup_form': SignupForm(),
        }
    )


def login(request):
    next_path = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            if next_path:
                return redirect(next_path)
            return redirect('post:post_list')
    else:
        form = LoginForm()
        # GET 요청에서는 LoginForm을 보여줌
    return render(
        request,
        'member/login.html',
        {
            'login_form': form,
            'facebook_app_id': settings.FACEBOOK_APP_ID,
        }
    )


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


@login_required
def profile(request):
    return HttpResponse(f'User profile page {request.user}')

def facebook_login(request):
    print(request.GET)
    print(request.POST)
    return HttpResponse(f'GET: {request.GET} <br>POST: {request.POST}')
