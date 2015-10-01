#! coding: utf-8

from django import forms

class MailForm(forms.Form):
    sender_name  = forms.CharField(label="Имя", max_length=150)
    email = forms.EmailField(label="Email")
    letter_title = forms.CharField(label="Тема", max_length=500)
    letter_text = forms.CharField(widget=forms.Textarea)
