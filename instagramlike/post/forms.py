from django import forms

__all__ = (
    'PostForm',
)
class PostForm(forms.Form):
    photo = forms.ImageField(required=True)
    text = forms.CharField(max_length=50)
