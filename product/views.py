from django.http import HttpRequest
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import authentication_classes, permission_classes

from .serializers import ProductSerializers, ProductRateSerializer
from .models import Product, Rate


class ProductListView(ListAPIView):
    serializer_class = ProductSerializers
    queryset = Product.objects.filter(available=True)


class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializers
    queryset = Product.objects.filter(available=True)
    lookup_field = "id"


class ProductPackageListView(ListAPIView):
    serializer_class = ProductSerializers
    queryset = Product.get_package


class ProductTakiListView(ListAPIView):
    serializer_class = ProductSerializers
    queryset = Product.get_taki


class ProductTonyListView(ListAPIView):
    serializer_class = ProductSerializers
    queryset = Product.get_tony


class ProductRatePostView(APIView):
    serializer_class = ProductRateSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        print(ser_data.data)
        print(request.user.id)
        Rate.objects.create(product_id=ser_data.validated_data["product_id"], user_id=request.user.id,
                            rate=ser_data.validated_data["rate"])
        return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
