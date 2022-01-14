import json
from django.http import HttpResponse
from .models import Offers
from django.core import serializers

def offers_list(request) -> HttpResponse:
    offers = {
        "offers": Offers.objects.values(),
        "pages" : 1,
        "current_page": 1,
    }

    print(offers)
    
    return HttpResponse("json.dumps(offers)", content_type='application/json')