from django import forms
from .models import PostComment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-right', 'placeholder': 'نام خود را وارد کنید'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-right', 'placeholder': 'ایمیل خود را وارد کنید'}),
            'body': forms.Textarea(attrs={'class': 'form-control text-right', 'placeholder': 'متن نظر خود را وارد کنید'}),

        }
