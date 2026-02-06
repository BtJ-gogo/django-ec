from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Order, OrderItem


class OrderModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testuser", email="testu@test.com", password="testpass"
        )
        cls.order = Order.objects.create(
            user=cls.user,
            name="test name",
            email="testu@test.com",
            phone="1234567890",
            zipcode="12345",
            state="Test State",
            city="Test City",
            address1="1-4-2 Test Address",
            address2="303",
            total_price=4500,
            stripe_id="123456789asdfas",
        )

    # Orderが正常に作成されるか
    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.name, "test name")
        self.assertEqual(self.order.email, "testu@test.com")
        self.assertEqual(self.order.phone, "1234567890")
        self.assertEqual(self.order.zipcode, "12345")
        self.assertEqual(self.order.state, "Test State")
        self.assertEqual(self.order.city, "Test City")
        self.assertEqual(self.order.address1, "1-4-2 Test Address")
        self.assertEqual(self.order.address2, "303")
        self.assertEqual(self.order.total_price, 4500)
        self.assertEqual(self.order.stripe_id, "123456789asdfas")

    # payment_statusのデフォルト値が'PE'（保留中）か
    def test_default_payment_status(self):
        self.assertEqual(self.order.payment_status, Order.PaymentStatus.PENDING)

    # shipping_statusのデフォルト値が'PE'（発送準備中）か
    def test_default_shipping_status(self):
        self.assertEqual(self.order.shipping_status, Order.ShippingStatus.PENDING)

    # dateが自動的に設定されるか
    def test_date_auto_now_add(self):
        self.assertIsNotNone(self.order.date)

    # __str__メソッドが正しいフォーマットを返すか
    def test_order_str(self):
        self.assertEqual(str(self.order), f"注文ID{self.order.id}")

    # blank test
    def test_blank(self):
        order = Order.objects.create(
            user=self.user,
            name="test name",
            email="testu@test.com",
            phone="1234567890",
            zipcode="12345",
            state="Test State",
            city="Test City",
            address1="1-4-2 Test Address",
            total_price=4500,
        )
        order.full_clean()

    # total_priceが負の値の場合にバリデーションエラーが発生するか
    def test_total_price_negative_validation(self):
        order = Order(
            user=self.user,
            name="test",
            email="test@test.com",
            phone="1234567890",
            zipcode="12345",
            state="Test",
            city="Test",
            address1="Test",
            total_price=-100,
        )
        with self.assertRaises(ValidationError):
            order.full_clean()

    # total_priceが0の場合は許可されるか
    def test_total_price_zero_is_valid(self):
        order = Order(
            user=self.user,
            name="test",
            email="test@test.com",
            phone="1234567890",
            zipcode="12345",
            state="Test",
            city="Test",
            address1="Test",
            total_price=0,
        )
        order.full_clean()  # エラーが発生しないことを確認
        order.save()
        self.assertEqual(order.total_price, 0)

    # PaymentStatusの各選択肢が正しく設定できるか
    def test_payment_status_choices(self):
        self.order.payment_status = Order.PaymentStatus.PAID
        self.order.save()
        self.assertEqual(self.order.payment_status, "PA")

    # ShippingStatusの各選択肢が正しく設定できるか
    def test_shipping_status_choices(self):
        self.order.shipping_status = Order.ShippingStatus.SHIPPED
        self.order.save()
        self.assertEqual(self.order.shipping_status, "SH")
