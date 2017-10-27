from django.contrib.auth import (
    get_user_model,
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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 중복이 없다면 User 생성
            user = User.objects.create_user(
                username=username,
                password=password,
            )
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
        # 로그인 실패 메시지 출력
        else:
            return HttpResponse('Login credentials invalid')
    else:
        # GET 요청에서는 LoginForm을 보여줌
        return render(
            request,
            'member/login.html',
        )
