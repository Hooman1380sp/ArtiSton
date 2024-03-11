from django.urls import path
from .views import ProductListView, ProductDetailView


app_name = "product"

urlpatterns = [
    path("list/",ProductListView.as_view()),
    path("detail/<int:id>/",ProductDetailView.as_view()),
]
