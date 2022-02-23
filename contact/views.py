from django.http import HttpRequest
from django.shortcuts import redirect
from django.views import View


class MailView(View):
    def get(self, request: HttpRequest):
        return "ok"

    def post(self, request: HttpRequest):
        print(request.POST)
        msg = " ok"
        return redirect(f"/enquiry?msg={msg}")

