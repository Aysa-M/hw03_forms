from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Класс для создания формы, предназначенной для создания нового поста.
    """
    class Meta:
        model = Post
        fields = ('text', 'group')
