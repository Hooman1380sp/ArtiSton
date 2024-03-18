from django.http import HttpRequest
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .serializers import ProductSerializer, ProductRatePostSerializer, DisCountSerializer
from .models import Product, Rate, DisCount


class ProductListView(ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(available=True)


class ProductDetailView(RetrieveAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(available=True)
    lookup_field = "id"


class ProductPackageListView(ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.get_package


class ProductRetailListView(ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.get_retail


class ProductWholeSaleListView(ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.get_wholesale


class ProductRatePostView(APIView):
    serializer_class = ProductRatePostSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        try:
            Rate.objects.create(product_id=ser_data.validated_data["product_id"], user_id=request.user.id,
                                rate=ser_data.validated_data["rate"])
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"message": f"Rate product and user must be unique, {e}"},
                            status=status.HTTP_501_NOT_IMPLEMENTED)


class DisCountListView(APIView):
    serializer_class = DisCountSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        ser_data = self.serializer_class(instance=DisCount.objects.all(), many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class NewSeasonListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.get_new_season
