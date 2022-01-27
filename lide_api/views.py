import json
from typing import Any, Dict, List
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views import View
from django.core.paginator import Paginator, Page
from django.db.models import Q
from .models import Offers



class OffersListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        params: Dict[str, Any] = self._get_parameters(request)

        offer_list = self._get_offers()
        paginator = Paginator(offer_list, per_page=params.get('items', 2), allow_empty_first_page=True)
        current_page: Page = paginator.get_page(params.get("page_no"))

        offers:Dict[str, Any] = {
            "results": self._get_current_page(current_page),
            "pages" : paginator.num_pages,
            "currentPage": current_page.number,
            "pageRange": list(paginator.get_elided_page_range(current_page.number)) 
        }
        return HttpResponse(json.dumps(offers, default=str, indent=4),
                            content_type='application/json', )

    def _get_parameters(self, request: HttpRequest) -> Dict[str, Any]:
        results:Dict[str, Any] = {}
        try:
            results["page_no"] = int(request.GET.get("page", "1"))
        except ValueError:
            results["page_no"] = 1
        return results

    def _get_offers(self):
        offer_list: List[Dict[Any, Any]] = list(Offers.objects.all().filter(posted__exact=True).order_by("-edited"))
        return offer_list

    def _get_current_page(self, current_page: Page) -> List[Dict[str, Any]]:
        result:List[Dict[str, Any]] = []
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
  
        
class OfferSearch(OffersListView):
                        
    def _get_parameters(self, request: HttpRequest) -> Dict[str, Any]:
        results:Dict[str, Any] = super()._get_parameters(request)
        try:
            results["query"] = str(request.GET.get("q", ""))
        except ValueError:
            results["page_no"] = 1
        return results

    def _get_offers(self, params):
        query = params.get(query)
        offer_list: List[Dict[Any, Any]] = list(Offers.objects.all().filter(posted__exact=True)
                                                                    .order_by("-edited")
                                                                    .filter(Q(position__name__icontains=query) | Q(location__name__icontains=query) | Q(employment_type__name__icontains=query) | Q(details__icontains=query))
                                                                    .distinct())
                                                                    
        return offer_list
        
    
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