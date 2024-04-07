from django import forms
from .models import PostComment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=80, label='نام خود را وارد کنید',
                           widget=forms.TextInput(attrs={'class': 'form-control form text-right'}))
    email = forms.EmailField(label='ایمیل خود را وارد کنید',
                             widget=forms.EmailInput(attrs={'class': 'form-control text-right'}))
    to = forms.EmailField(label='ایمیل خود را وارد کنید',
                          widget=forms.EmailInput(attrs={'class': 'form-control text-right'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control text-right'}),
                               label='متن نظر خود را وارد کنید')


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-right', 'placeholder': 'نام خود را وارد کنید'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control text-right', 'placeholder': 'ایمیل خود را وارد کنید'}),
            'body': forms.Textarea(
                attrs={'class': 'form-control text-right', 'placeholder': 'متن نظر خود را وارد کنید'}),

        }


class SearchForm(forms.Form):
    query = forms.CharField()
