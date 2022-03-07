from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import redirect
from django.views import View
from django import forms
from .forms import MessageForm
from .models import Message
import requests
from settings.models import Settings


class MailView(View):
    def get(self, request: HttpRequest):
        return "ok"

    def post(self, request: HttpRequest):
        msg = "ok"
        secret = Settings.objects.get(name__exact="grecaptcha")
        msg_form = MessageForm(request.POST)
        if msg_form.is_valid():
            token = msg_form.cleaned_data.get("google_recaptcha")
            resp = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                {"secret": secret.value, "response": token},
            )

            ret = resp.json()
            print(ret)
            if ret["success"] and ret["score"] > 0.5 and ret["action"] == "submit":
                # self.save_msg(msg_form)
                return self._mail(msg_form)
            else:
                msg = " ".join(ret["error-codes"])
        return redirect(f"/enquiry?msg={msg}")

    def save_msg(self, msg_form: forms.Form):
        msg_obj = Message()
        msg_obj.iam = msg_form.cleaned_data.get("iam")
        msg_obj.fname = msg_form.cleaned_data.get("fname")
        msg_obj.lname = msg_form.cleaned_data.get("lname")
        msg_obj.email = msg_form.cleaned_data.get("email")
        msg_obj.phone = msg_form.cleaned_data.get("phone")
        msg_obj.msg = msg_form.cleaned_data.get("msg")
        msg_obj.save()

    def _mail(self, msg_form: forms.Form):

        to_email_list = [
            mail.value
            for mail in Settings.objects.all().filter(name__exact="contact_mail")
        ]
        if not to_email_list:
            print("Contact email not found")
            return
        msg: str = f"""
        Jestem : {msg_form.cleaned_data.get("iam")}
        Imię : {msg_form.cleaned_data.get("fname")}
        Nazwisko : {msg_form.cleaned_data.get("lname")}
        Email : {msg_form.cleaned_data.get("email")}
        Telefon : {msg_form.cleaned_data.get("phone")}
        Wiadomość : {msg_form.cleaned_data.get("msg")}
        """
        subject = f'{msg_form.cleaned_data.get("iam")} - {msg_form.cleaned_data.get("fname")} {msg_form.cleaned_data.get("lname")}'

        try:
            send_mail(subject, msg, "info@angrysoft.ovh", to_email_list)
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

        return HttpResponseRedirect("/")
