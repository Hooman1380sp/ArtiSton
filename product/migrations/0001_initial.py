# Generated by Django 5.0.3 on 2024-03-10 13:31

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProductGallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="Gallery_Product")),
            ],
        ),
        migrations.CreateModel(
            name="TypeSell",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=256)),
            ],
            options={
                "verbose_name": "Type Sell",
                "verbose_name_plural": "Type Sells",
            },
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="products"),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.productcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Category",
                "verbose_name_plural": "Product Categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title_arabic",
                    models.CharField(max_length=256, verbose_name="Arabic Title"),
                ),
                (
                    "title_english",
                    models.CharField(max_length=256, verbose_name="English Title"),
                ),
                (
                    "description_arabic",
                    models.TextField(max_length=1024, verbose_name="Arabic Title"),
                ),
                (
                    "description_english",
                    models.TextField(max_length=1024, verbose_name="English Title"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=3, max_digits=9, verbose_name="Price"
                    ),
                ),
                ("available", models.BooleanField(default=True)),
                ("new_season", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="back_category",
                        to="product.productcategory",
                        verbose_name="Category",
                    ),
                ),
                (
                    "gallery",
                    models.ManyToManyField(
                        related_name="back_gallery",
                        to="product.productgallery",
                        verbose_name="Gallery",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
    ]
