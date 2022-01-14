from rest_framework import serializers
from .models import Offers


class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = [
            'position',
            'location',
            'employment_type',
            
        ]