from django.contrib import admin

from contact.models import MailSettings, Message

# Register your models here.

admin.site.register(Message)
admin.site.register(MailSettings)
