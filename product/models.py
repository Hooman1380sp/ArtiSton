from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.

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
    product = models.ForeignKey(to='Product',on_delete=models.CASCADE,related_name="type_product")

    class Meta:
        verbose_name = "Type Sell"
        verbose_name_plural = "Type Sells"

    def __str__(self):
        return self.title


class Product(models.Model):
    title_arabic = models.CharField(max_length=256, verbose_name="Arabic Title")
    title_english = models.CharField(max_length=256, verbose_name="English Title")
    description_arabic = models.TextField(max_length=1024, verbose_name="Arabic Title")
    description_english = models.TextField(max_length=1024, verbose_name="English Title")
    price = models.DecimalField(verbose_name="Price", max_digits=9, decimal_places=3)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name="Category",
                                 related_name="back_category")
    gallery = models.ManyToManyField(to='ProductGallery', verbose_name="Gallery", related_name="back_gallery")
    available = models.BooleanField(default=True)
    new_season = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title_english} - {self.description_english[:30]}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductGallery(models.Model):
    image = models.ImageField(upload_to="Gallery_Product")

    def __str__(self):
        return f"{self.id}"
