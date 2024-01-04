from rest_framework import serializers
from .models import Product
from rest_framework.response import Response
from rest_framework import status

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'