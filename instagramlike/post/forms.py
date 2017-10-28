from django import forms

from post.models import Post

__all__ = (
    'PostForm',
)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'photo',
        )

    def save(self, commit=True, *args, **kwargs):
        # 처음 Post객체가 만들어질 때 author필드가 비어있으면 save(commit=True)를 비허용
        # instance 생성(commit=False)허용하고,
        # save()에 author키워드 인수값을 전달할 수 있도록 save()메서드 재정의
        # 새로 저장하려는 instance는 pk값이 없다.
        if not self.instance.pk and commit:
            # author값을 키워드인수 묶음에서 pop으로 삭제하며 값을 가져온다
            author = kwargs.pop('author', None)
            if not author:
                raise ValueError('Author field is required')
            self.instance.author = author
        return super().save(*args, **kwargs)



class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
