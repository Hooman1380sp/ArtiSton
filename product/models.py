from zoneinfo import available_timezones

from django.db import models
from django.db.models import Avg
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django_cleanup import cleanup


@cleanup.select
class ProductCategory(MPTTModel):
    title = models.CharField(max_length=256)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="products", null=True, blank=True, help_text="")

    class MPTTMeta:
        order_insertions_by = ["name"]

    def __str__(self):
        return f"{self.title} - {self.id}"

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class TypeSell(models.Model):
    title = models.CharField(max_length=256)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name="type_product")

    class Meta:
        verbose_name = "Type Sell"
        verbose_name_plural = "Type Sells"

    def __str__(self):
        return self.title


@cleanup.select
class Product(models.Model):
    title_arabic = models.CharField(max_length=256, verbose_name="Arabic Title")
    title_english = models.CharField(max_length=256, verbose_name="English Title")
    description_arabic = models.TextField(max_length=1024, verbose_name="Arabic Description")
    description_english = models.TextField(max_length=1024, verbose_name="English Description")
    price = models.DecimalField(verbose_name="Price", max_digits=9, decimal_places=3)
    detail_arabic = models.TextField(max_length=512, verbose_name="Detail_Arabic")
    detail_english = models.TextField(max_length=512, verbose_name="Detail_English")
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name="Category",
                                 related_name="back_category")
    gallery = models.ManyToManyField(to='ProductGallery', verbose_name="Gallery", related_name="back_gallery")
    available = models.BooleanField(default=True)
    new_season = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title_english} - {self.description_english[:30]}"

    @property
    def get_package(self):
        return Product.objects.filter(available=True, type_product__title="package")

    @property
    def get_wholesale(self):
        return Product.objects.filter(available=True, type_product__title="wholesale")

    @property
    def get_retail(self):
        return Product.objects.filter(available=True, type_product__title="retail")

    @property
    def get_new_season(self):
        return Product.objects.filter(available=True, new_season=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


@cleanup.select
class ProductGallery(models.Model):
    image = models.ImageField(upload_to="Gallery_Product/")

    def __str__(self):
        return f"{self.id}"


class Rate(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="Product",
                                related_name="Rate_Product_back")
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name="User")
    rate = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name="Rate")

    class Meta:
        unique_together = ('product', 'user')

    @property
    def average_rate(self):
        return Rate.objects.filter(product_id=self.product.id).aggregate(average_rate=Avg('rate'))['average_rate']

    def __str__(self):
        return self.average_rate


class DisCount(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="back_discount_product")
    discount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title_english[:35]} - {self.discount}"
