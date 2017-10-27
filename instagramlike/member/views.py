from django.contrib.auth import (
    get_user_model,
    authenticate,
    login as django_login,
)
from django.http import HttpResponse
from django.shortcuts import render, redirect

from member.forms import SignupForm

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
        # 회원 인증 절차
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        print('user: ', user)
        # 가입 회원이라면,
        if  user:
            # 해당 유저의 정보를 Django의 Session에 추가하고,
            # Django 앱서버는 SessionKey값을  Set-Cookie 헤더에 담아서 보냄
            # 유저의 브라우저는 위 Cookie를 받아 저장하고, 이후 요청할 때 Django 앱서버에 보내
            # 로그인을 유지함
            django_login(request, user)
            # 로그인이 유지되면 post_list.html로 돌아감
            return redirect('post:post_list')
        # 로그인 실패 메시지 출력
        return HttpResponse('Login credentials invalid')
    # GET 요청에서는 LoginForm을 보여줌
    return render(
        request,
        'member/login.html',
    )

