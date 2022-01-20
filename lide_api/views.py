import json
from typing import Any, Dict, List
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views import View
from django.core.paginator import Paginator, Page
from .models import Offers


class OffersView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            page_no:int = int(request.GET.get("page", "1"))
        except ValueError:
            page_no: int = 1

        offer_list: List[Dict[Any, Any]] = list(Offers.objects.all().filter(posted__exact=True).order_by("-edited"))
        paginator = Paginator(offer_list, per_page=2, allow_empty_first_page=True)
        current_page: Page = paginator.get_page(page_no)
        # current_page = paginator.page(1)
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

class OfferDetails(View):
    def get(self, request: HttpRequest, offer_id:int = -1) -> HttpResponse:
    
        offer = get_object_or_404(Offers.objects.filter(posted__exact=True), id=offer_id)
        result = {
                "id": offer.pk,
                "position": offer.position,
                "location": list(offer.location.all()),
                "employmentType": list(offer.employment_type.all()),
                "details": offer.details,
                "edited": offer.edited
            }

        return HttpResponse(json.dumps(result, default=str, indent=4),
                            content_type='application/json', )
        
