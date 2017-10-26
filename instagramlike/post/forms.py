from django import forms

__all__ = (
    'PostForm',
)


class PostForm(forms.Form):
    photo = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    text = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
    )
