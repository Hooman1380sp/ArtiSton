from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import ProductSerializers
from .models import Product


class ProductListView(ListAPIView):
    serializer_class = ProductSerializers
    queryset = Product.objects.filter(available=True)


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializers
    queryset = Product.objects.filter(available=True)
    lookup_field = "id"
