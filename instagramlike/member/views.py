from pprint import pprint
from typing import NamedTuple

import requests
from django.contrib.auth import (
    get_user_model,
    logout as django_logout,
    login as django_login,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

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
            'scope': settings.FACEBOOK_SCOPE,
        }
    )


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


@login_required
def profile(request):
    return HttpResponse(f'User profile page {request.user}')


# 1. 사용자가 앱 사이트에서 '페이스북 로그인' 버튼을 클릭
# 2. 앱 사이트는 '사용자가  페이스북 가서 로그인하고 응답을 받아오도록 ' 페이스북 대화상자로  리디렉션
# 3. 사용자는 페이스북 대화상자에서 로그인을 하고 앱 사이트 접근권한을 얻음
# 4. 페이스북은 브라우저에게  로그인 정보(code)와 함께 redirect_uri위치로 리디렉션할 것을 요청함
# 5. 요청받은 브라우저는 앱 사이트(redirect_uri)에 GET요청함
# 6. 앱사이트는  GET요청에 포함된 code를 이용하여 페이스북에 access_token을 요청함
# 7. 페이스북이 앱사이트에 access_token을 돌려줌
def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', ' ')
            self.url_picture = data['picture']['data']['url']

    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'

    # 접근권한을 얻는 함수
    def get_access_token_info(code_value):
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login'),
        )
        # ID확인: 액세스 토큰의 코드 교환 : OAuth 엔드포인트에 HTTP GET 요청
        response = requests.get(
            'https://graph.facebook.com/v2.10/oauth/access_token',
            {
                'client_id': app_id,
                'redirect_uri': redirect_uri,
                'client_secret': app_secret_code,
                'code': code_value,
            }
        )
        return AccessTokenInfo(**response.json())

    # 액세스 토큰 검사 함수
    def get_debug_token_info(token):
        response = requests.get(
            'https://graph.facebook.com/debug_token',
            {
                # 검사가 필요한 토큰
                'input_token': token,
                # 앱 개발자의 액세스 토큰 (앱 엑세스 토큰)
                'access_token': app_access_token,
            }
        )
        return DebugTokenInfo(**response.json()['data'])

    # code값을 전달받아 access_token값을 가져오기
    code = request.GET.get('code')
    access_token = get_access_token_info(code).access_token
    # access_token이 유효한지 검사하기
    debug_token_info = get_debug_token_info(access_token)

    # 유저 정보 가져오기  >>  문서: 그래프 API >> 도구및 지원: 그래프 API탐색기
    response = requests.get(
        'https://graph.facebook.com/me',
        {
            'fields': 'id,name,picture,email',
            'access_token': access_token,
        }
    )
    result = response.json()
    user_info = UserInfo(data=result)

    # 페이스북으로 가입한 유저의 username:  fb_<facebook_user_id>
    username = f'fb_{user_info.id}'
    # 위 username에 해당하는 User가 있는지 검사
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
            age=0
        )
    django_login(request, user)
    return redirect('post:post_list')
