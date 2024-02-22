from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from posts.models import Post,Comment, Tag

class PostCreateForm(forms.ModelForm):
    tags = forms.SelectMultiple(choices=Tag.objects.all())
    class Meta:
        model = Post
        fields = ['picture','title','text','tags']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', )


