from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render


User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            # username 중복 막기
            if User.objects.filter(username=username).exist():
                return HttpResponse(f'Username {username} is already exist')
            # 중복이 없다면 User 생성
            user = User.objects.create_user(
                username=username,
                password=password
            )
            return HttpResponse(f'{user.username}, {user.password}')
    return render(request, 'member/signup.html')

