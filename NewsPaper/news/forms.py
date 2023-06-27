from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    # postAuthor = forms.ChoiceField()
    title = forms.CharField(max_length=150)
    text = forms.TextInput()

    class Meta:
        model = Post
        fields = ['postCategory','title','text']
        # exclude = ['postType', 'rating']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Текст не может быть менее 20 символов."
            })

        return cleaned_data


class NewArticle(forms.ModelForm):
    text = forms.CharField(min_length=50)

    class Meta:
        model = Post
        exclude = ['postType', 'rating']
