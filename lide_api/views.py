from rest_framework import viewsets
from .serializer import OffersSerializer
from .models import Offers

class OffersView(viewsets.ModelViewSet):
    serializer_class = OffersSerializer
    queryset = Offers.objects.all()