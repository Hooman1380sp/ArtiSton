from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BlogSerializer
from .models import Blog


class BlogListView(ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = BlogSerializer
    queryset = Blog.List_Blog


class BlogDetailView(APIView):
    serializer_class = BlogSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, id):
        ser_data = self.serializer_class(instance=get_object_or_404(Blog, id=id))
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
