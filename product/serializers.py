from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import ProductCategory, Product, ProductGallery, TypeSell, Rate, DisCount


class ProductRateGetSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    average_rate = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = ["product_id", "rate", "average_rate"]
        read_only_fields = ['average_rate']

    def get_average_rate(self, obj):
        return obj.average_rate


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    # rate = serializers.SerializerMethodField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rate = ProductRateGetSerializer(many=True, read_only=True, source='Rate_Product_back',
                                    validators=[[MinValueValidator(1), MaxValueValidator(5)]])

    class Meta:
        model = Product
        fields = (
            "title_arabic", "title_english", "description_arabic", "description_english", "detail_arabic",
            "detail_english",
            "price", "images", "id", "rate")

    def get_images(self, obj):
        result = obj.gallery.all()
        return ProductGallerySerializer(instance=result, many=True).data

    def get_rate(self, obj):
        result = obj.Rate_Product_back.filter(product_id=obj.id)
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


class ProductRatePostSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = Rate
        fields = ["product_id", "rate", "average_rate"]


class DisCountSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = DisCount
        fields = ("products", "discount")

    def get_products(self, obj: DisCount):
        res = Product.objects.filter(back_discount_product__isnull=False)
        return ProductSerializer(instance=res, many=True).data
