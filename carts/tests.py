from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from .models import Cart
from products.models import Author, Book, Category


class CartModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser", email="testu@test.com", password="testpass"
        )
        cls.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        cls.author = Author.objects.create(
            name="Test Author",
            kana_name="テストオーサー",
            birth_date="2000-01-01",
            bio="Test bio",
        )
        cls.book = Book.objects.create(
            category=cls.category,
            name="Test Book",
            author=cls.author,
            publisher="test",
            published_at="1999-12-12",
            price=1000,
            description="test",
            stock=5,
            status=Book.Status.ACTIVE,
        )
        cls.cart = Cart.objects.create(
            user=cls.user,
            product=cls.book,
            quantity=2,
        )

    # 正常にカートが作成されているか
    def test_create_cart(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(self.cart.product, self.book)
        self.assertEqual(self.cart.quantity, 2)

    # get_total_priceメソッドの動作確認
    def test_get_total_price(self):
        expected_total = self.book.price * self.cart.quantity
        self.assertEqual(self.cart.get_total_price(), expected_total)

    # unique_together制約の確認
    def test_unique_together_constraint(self):
        with self.assertRaises(IntegrityError):
            cart = Cart.objects.create(
                user=self.user,
                product=self.book,
                quantity=1,
            )

    # quantityが1未満の場合のバリデーションエラー確認
    def test_quantity_min_value_validation(self):
        cart = Cart(
            user=self.user,
            product=self.book,
            quantity=0,
        )
        with self.assertRaises(ValidationError):
            cart.full_clean()
