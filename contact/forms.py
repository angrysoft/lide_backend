import email
from django import forms


class MessageForm(forms.Form):
    google_recaptcha = forms.CharField()
    iam = forms.CharField()
    fname = forms.CharField()
    lname = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    msg = forms.Textarea()
    rodo = forms.BooleanField()
