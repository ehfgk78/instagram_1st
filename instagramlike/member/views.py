from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

from member.forms import SignupForm

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        # SignupForm에 바인딩된 request.POST
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # username 중복 막기
            if User.objects.filter(username=username).exist():
                return HttpResponse(f'Username {username} is already exist')
            # 중복이 없다면 User 생성
            user = User.objects.create_user(
                username=username,
                password=password
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

