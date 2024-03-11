from django.contrib import admin
from .models import Product, ProductGallery, ProductCategory, TypeSell


# class ProductCategoryAdmin(admin.TabularInline):  # یا admin.StackedInline برای نمایش متفاوت
#     model = ProductCategory
#     extra = 1  # تعداد فرم‌های اضافی برای افزودن رکوردهای جدید
#
#
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductCategory, ]


admin.site.register(Product)
admin.site.register(ProductGallery)
admin.site.register(ProductCategory)

