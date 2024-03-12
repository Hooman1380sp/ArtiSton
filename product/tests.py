from django.test import TestCase

from .models import Product, ProductCategory, ProductGallery, TypeSell


class ProductTests(TestCase):

    def setUp(self):
        self.category = ProductCategory.objects.create(title="test_category_product", image="test_category_Product.png")
        self.type_sell = TypeSell.objects.create(title="test_type_sell")
        self.product_gallery = ProductGallery.objects.create(image="test_product_gallery.png")
        self.product = Product.objects.create(title_arabic="al_test_product", title_english="en_test_product",
                                              description_arabic="test_al_des", description_english="test_en_des",
                                              category=self.category, price=10000.345)
        self.product.gallery.add(self.product_gallery)

    def test_product(self):
        self.assertEqual(self.product.title_arabic, "al_test_product")
        self.assertEqual(self.product.title_english, "en_test_product")
        self.assertEqual(self.product.description_arabic, "test_al_des")
        self.assertEqual(self.product.description_english, "test_en_des")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, 10000.345)
        self.assertIn(self.product_gallery, self.product.gallery.all())
        self.assertTrue(self.product.available)
        self.assertFalse(self.product.new_season)

    def test_category(self):
        self.assertEqual(self.category.title, 'test_category_product')
        self.assertEqual(self.category.image, 'test_category_Product.png')

    def test_typeSell(self):
        self.assertEqual(self.type_sell.title, "test_type_sell")

    def test_productGallery(self):
        self.assertEqual(self.product_gallery.image, "test_product_gallery.png")
