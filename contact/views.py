from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class MailView(View):
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        print(request.POST)
