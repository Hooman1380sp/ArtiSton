from django.contrib import admin
from .models import Product, ProductGallery, ProductCategory, TypeSell, DisCount


class TypeSellInline(admin.StackedInline):
    model = TypeSell


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [TypeSellInline]


admin.site.register(ProductGallery)
admin.site.register(ProductCategory)
admin.site.register(TypeSell)
admin.site.register(DisCount)
