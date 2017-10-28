from django import forms
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login as django_login,
)
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 초기화 과정에서 attrs를 업데이트할 필드 이름 목록
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'img_profile',
            'age',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    # 중복 유저 검사
    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('으아아아아')
        return data

    # password 확인
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password2

    # 회원가입 완료 전 마지막 유효성 검사
    def clean(self):
        if self.is_valid():
            setattr(self, 'signup', self._signup)
        return self.cleaned_data

    def _signup(self):
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            age=self.cleaned_data['age']
        )


class LoginForm(forms.Form):
    """
    is_valid()에서 주어진 username/password를 사용한 authenticate실행
    성공시 login(request)메서드를 사용할 수 있음
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        # cleaned_data = super().clean()
        # 해당 유저가 있는지 인증
        self.user = authenticate(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password')
        )
        # 인증 안되면 에러 발생
        if not self.user:
            raise forms.ValidationError('Invalid login credentials')
        else:
            setattr(self, 'login', self._login)

    def _login(self, request):
        django_login(request, self.user)
