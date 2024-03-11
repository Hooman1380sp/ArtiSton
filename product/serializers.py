from rest_framework import serializers
from .models import ProductCategory, Product, ProductGallery, TypeSell


class ProductSerializers(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("title_arabic", "title_english", "description_arabic", "description_english", "price","images","id")

    def get_images(self, obj):
        result = obj.gallery.all()
        return ProductGallerySerializer(instance=result, many=True).data

# clas


class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ("image",)
