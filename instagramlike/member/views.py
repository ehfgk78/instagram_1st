from django.contrib.auth import (
    get_user_model,
    logout as django_logout,
)
from django.http import HttpResponse
from django.shortcuts import render, redirect

from member.forms import SignupForm, LoginForm

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        # SignupForm에 바인딩된 request.POST
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.signup()
            return HttpResponse(f'{user.username}, {user.password}')
            # GET요청시  비어있는 SignupForm을 전달
    return render(
        request,
        'member/signup.html',
        {
            'form': SignupForm(),
        }
    )


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('post:post_list')
    else:
        form = LoginForm()
        # GET 요청에서는 LoginForm을 보여줌
    return render(
        request,
        'member/login.html',
        {
            'login_form': form,
        }
    )

def logout(request):
    django_logout(request)
    return redirect('post:post_list')