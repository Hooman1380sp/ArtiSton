from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BlogSerializer
from .models import Blog


# class BlogListView(APIView):
#     serializer_class = BlogSerializer
#
#     def get(self, request):
#         ser_data = self.serializer_class(instance=Blog.List_Blog, many=True)
#         return Response(data=ser_data.data, status=status.HTTP_200_OK)


class BlogListView(ListAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.List_Blog


class BlogDetailView(APIView):
    serializer_class = BlogSerializer

    def get(self, request, id):
        ser_data = self.serializer_class(instance=get_object_or_404(Blog, id=id))
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
