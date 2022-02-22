from os import abort
from typing import Any, Dict, List
from django.http import Http404, HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.core.paginator import Paginator, Page
from django.db.models import Q
from .models import Offers, Posts, Pages, Contacts


class GenericListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        params: Dict[str, Any] = self._get_parameters(request)

        items_list: list[Dict[Any, Any]] = self._get_items(params)
        paginator = Paginator(
            items_list, per_page=params.get("items", 10), allow_empty_first_page=True
        )
        current_page: Page = paginator.get_page(params.get("page_no"))

        result: Dict[str, Any] = {
            "results": self._get_current_page(current_page),
            "pages": paginator.num_pages,
            "currentPage": current_page.number,
            "pageRange": list(paginator.get_elided_page_range(current_page.number)),
        }

        return JsonResponse(result, safe=False)

    def _get_items(self, params: Dict[str, Any]) -> list[Dict[Any, Any]]:

        return []

    def _get_parameters(self, request: HttpRequest) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        try:
            results["page_no"] = int(request.GET.get("page", "1"))
        except ValueError:
            results["page_no"] = 1
        try:
            results["items"] = int(request.GET.get("items", 10))
        except ValueError:
            results["items"] = 10

        return results

    def _get_current_page(self, current_page: Page) -> List[Dict[str, Any]]:
        return []


class OffersListView(GenericListView):
    def _get_items(self, params: Dict[str, Any]) -> list[Dict[Any, Any]]:
        offer_list: List[Dict[Any, Any]] = list(
            Offers.objects.all().filter(posted__exact=True).order_by("-edited")
        )
        return offer_list

    def _get_current_page(self, current_page: Page) -> List[Dict[str, Any]]:
        return [offer.serialize_short() for offer in current_page.object_list]


class OfferDetails(View):
    def get(self, request: HttpRequest, offer_id: int = -1) -> HttpResponse:

        offer = get_object_or_404(
            Offers.objects.filter(posted__exact=True), id=offer_id
        )

        return JsonResponse(offer.serialize(), safe=False)


class OfferSearch(OffersListView):
    def _get_parameters(self, request: HttpRequest) -> Dict[str, Any]:
        results: Dict[str, Any] = super()._get_parameters(request)
        results["query"] = str(request.GET.get("q", ""))
        return results

    def _get_items(self, params: Dict[str, Any]):
        query: str = params.get("query", "")
        offer_list: List[Dict[Any, Any]] = list(
            Offers.objects.all()
            .filter(posted__exact=True)
            .order_by("-edited")
            .filter(
                Q(position__name__icontains=query)
                | Q(location__name__icontains=query)
                | Q(employment_type__name__icontains=query)
                | Q(details__icontains=query)
            )
            .distinct()
        )

        return offer_list


class PostsListView(GenericListView):
    def _get_items(self, params: Dict[str, Any]) -> list[Dict[Any, Any]]:
        posts_list: List[Dict[Any, Any]] = list(
            Posts.objects.all().filter(posted__exact=True).order_by("-edited")
        )
        return posts_list

    def _get_current_page(self, current_page: Page) -> List[Dict[str, Any]]:
        return [post.serialize_short() for post in current_page.object_list]


class PostDetails(View):
    def get(self, request: HttpRequest, post_id: int = -1) -> HttpResponse:

        post = get_object_or_404(Posts.objects.filter(posted__exact=True), id=post_id)
        return JsonResponse(post.serialize(), safe=False)


class Page(View):
    def get(self, request: HttpRequest, slug: str = "") -> HttpResponse:

        page = get_object_or_404(Pages.objects.filter(slug__exact=slug))
        return JsonResponse(page.serialize(), safe=False)


class ContactsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not (contacts := Contacts.objects.all()):
            raise Http404

        return JsonResponse([contact.serialize() for contact in contacts], safe=False)
