from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (ProductListView,
                    ProductDetailView,
                    ProductPackageListView,
                    ProductRetailListView,
                    ProductWholeSaleListView,
                    ProductRatePostView,
                    DisCountListView,
                    NewSeasonListView)

app_name = "product"

urlpatterns = [
    path("list/", ProductListView.as_view()),
    path("detail/<int:id>/", ProductDetailView.as_view()),
    path("package/", ProductPackageListView.as_view()),
    path("retail/", ProductRetailListView.as_view()),
    path("whole-sale/", ProductWholeSaleListView.as_view()),
    path("post-rate/", ProductRatePostView.as_view()),
    path("discount/", DisCountListView.as_view()),
    path("new-season/", NewSeasonListView.as_view()),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
