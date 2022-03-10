from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.core.mail import BadHeaderError, send_mail
from django.views import View
from django import forms
from .forms import MessageForm
from .models import Message
import requests
from settings.models import Settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class MailView(View):
    def get(self, request: HttpRequest):
        return HttpResponse("ok")

    def post(self, request: HttpRequest):
        msg = "ok"
        secret = Settings.objects.get(name__exact="grecaptcha")
        msg_form = MessageForm(request.POST)
        print(request.POST)
        if msg_form.is_valid():
            token = msg_form.cleaned_data.get("google_recaptcha")
            resp = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                {"secret": secret.value, "response": token},
            )

            ret = resp.json()
            print(ret)
            if ret["success"] and ret["score"] > 0.5 and ret["action"] == "submit":
                self.save_msg(msg_form)
                return self._mail(msg_form)
            else:
                msg = " ".join(ret["error-codes"])
                return HttpResponseBadRequest(msg)
        else:
            print(msg_form.errors)
            msg = "invalid data"
            return HttpResponseBadRequest(msg)

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
            send_mail(subject, msg, settings.EMAIL_HOST_USER, to_email_list)
        except BadHeaderError:
            return HttpResponse("Invalid header found.")

        return HttpResponseRedirect("/")
