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
    """
    get object product with id field
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(available=True)
    lookup_field = "id"


class ProductPackageListView(ListAPIView):
    """
    whole product that have tage(type sale package)
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.get_package


class ProductRetailListView(ListAPIView):
    """
    whole product that have tage(type sale retail)
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.get_retail


class ProductWholeSaleListView(ListAPIView):
    """
    whole product that have tage(type sale wholesale)
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.get_wholesale


class ProductRatePostView(APIView):
    """
    we got tow filed 1(rate(int)) and 2(product_id(int))
    and save in db this request with one user
    [Attention: sure must be unique (user and product) cause we have org average]
    """
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
    """
    list whole product that has discount!
    """
    serializer_class = DisCountSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        ser_data = self.serializer_class(instance=DisCount.objects.all(), many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class NewSeasonListView(ListAPIView):
    """
    whole product that is new season
    """

    serializer_class = ProductSerializer
    queryset = Product.get_new_season
