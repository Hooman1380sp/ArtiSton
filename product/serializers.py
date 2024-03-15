from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from .models import ProductCategory, Product, ProductGallery, TypeSell, Rate


class ProductSerializers(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    rate = serializers.StringRelatedField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        model = Product
        fields = (
            "title_arabic", "title_english", "description_arabic", "description_english", "detail_arabic",
            "detail_english",
            "price", "images", "id", "rate")

    def get_images(self, obj):
        result = obj.gallery.all()
        return ProductGallerySerializer(instance=result, many=True).data


class ProductGallerySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductGallery
        fields = ("image",)

    def get_image(self, obj):
        """ just get url (no base url(domain))
        """
        return f'/product/media/{obj.image}'


class ProductRateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = Rate
        fields = ["product_id", "rate"]

# class TokenObtainPairSerializer(TokenObtainPairSerializer):
#     def get_token(cls, user):
#         token = super().get_token(user)
