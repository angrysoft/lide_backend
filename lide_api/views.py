import json
from typing import Any, Dict, List
from wsgiref import headers
from django.http import HttpResponse, HttpRequest
from django.views import View
from django.core.paginator import Paginator, Page
from .models import Offers


class OffersView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page_no:int = 1
        offer_list: List[Dict[Any, Any]] = list(Offers.objects.all()) #.filter(posted__exact=True).order_by("post_date")
        paginator = Paginator(offer_list, per_page=10, allow_empty_first_page=True)
        # current_page: Page = paginator.get_page(page_no)
        current_page = paginator.page(1)
        offers:Dict[str, Any] = {
            "results": self.get_current_page(current_page),
            "pages" : paginator.num_pages,
            "current_page": current_page.number,
            "page_range": list(paginator.get_elided_page_range(current_page.number))
            
        }
        return HttpResponse(json.dumps(offers, default=str, indent=4),
                            content_type='application/json', )
                            # headers = {'Access-Control-Allow-Origin':"*"})

    def get_current_page(self, current_page: Page) -> List[Dict[str, Any]]:
        result = []
        for offer in current_page.object_list:
            result.append({
                "id": offer.pk,
                "position": offer.position,
                "location": list(offer.location.all()),
                "employmentType": list(offer.employment_type.all()),
                "edited": offer.edited
            }) 
        return result
