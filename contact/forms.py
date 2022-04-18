import email
from django import forms


class MessageForm(forms.Form):
    google_recaptcha = forms.CharField()
    iam = forms.CharField()
    fname = forms.CharField()
    lname = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    msg = forms.CharField(widget=forms.Textarea)
    rodo = forms.BooleanField()
    cv = forms.FileField(required=False)
    job = forms.IntegerField(required=False)
