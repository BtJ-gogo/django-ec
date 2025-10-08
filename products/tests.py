from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from accounts.models import CustomUser, Favorite
from products.models import Book, Author, Category


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )

    def test_str_method(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_name(self):
        self.assertEqual(self.category.name, "Test Category")

    def test_slug(self):
        self.assertEqual(self.category.slug, "test-category")

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Test Category", slug="another-slug")

    def test_unique_slug(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Another Category", slug="test-category")

    def test_max_length_name(self):
        test_data = Category(name="a" * 101, slug="test-slug")
        with self.assertRaises(ValidationError):
            test_data.full_clean()

    def test_max_length_slug(self):
        test_data = Category(name="Test Category", slug="a" * 101)
        with self.assertRaises(ValidationError):
            test_data.full_clean()


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(
            name="Test Author",
            kana_name="テストオーサー",
            birth_date="2000-01-01",
            bio="Test bio",
        )

    def test_name(self):
        self.assertEqual(self.author.name, "Test Author")

    def test_kana_name(self):
        self.assertEqual(self.author.kana_name, "テストオーサー")

    def test_birth_date(self):
        self.assertEqual(str(self.author.birth_date), "2000-01-01")

    def test_birth_date_ivalid(self):
        test_data = Author(
            name="Test Author",
            kana_name="テストオーサー",
            birth_date="2030-10-05",
            bio="Test bio",
        )
        with self.assertRaises(ValidationError):
            test_data.full_clean()

    def test_bio(self):
        self.assertEqual(self.author.bio, "Test bio")

    def test_str_method(self):
        self.assertEqual(str(self.author), "Test Author")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.author.get_absolute_url(),
            reverse("products:author_detail", kwargs={"pk": self.author.pk}),
        )

    def test_max_length_name(self):
        test_data = Author(
            name="a" * 101,
            kana_name="テストオーサー",
            birth_date="2000-01-01",
            bio="Test bio",
        )
        with self.assertRaises(ValidationError):
            test_data.full_clean()

    def test_max_lenght_kana_name(self):
        test_data = Author(
            name="Test Author",
            kana_name="a" * 51,
            birth_date="2000-01-01",
            bio="Test bio",
        )
        with self.assertRaises(ValidationError):
            test_data.full_clean()

    def test_blank_kana_name(self):
        test_data = Author(name="Test Author", birth_date="2000-02-02", bio="Test bio")
        test_data.full_clean()

    def test_blank_bio(self):
        test_data = Author(
            name="Test Author", kana_name="テストオーサー", birth_date="2000-02-02"
        )
        test_data.full_clean()

    def test_blank_fields(self):
        test_data = Author(name="Test Author", birth_date="2000-02-02")
        test_data.full_clean()


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_category(self):
        self.assertEqual(self.book.category, self.category)

    def test_name(self):
        self.assertEqual(self.book.name, "Test Book")

    def test_author(self):
        self.assertEqual(self.book.author, self.author)

    def test_publisher(self):
        self.assertEqual(self.book.publisher, "test")

    def test_published_at(self):
        self.assertEqual(str(self.book.published_at), "1999-12-12")

    def test_price(self):
        self.assertEqual(self.book.price, 1000)

    def test_description(self):
        self.assertEqual(self.book.description, "test")

    def test_stock(self):
        self.assertEqual(self.book.stock, 5)

    def test_status(self):
        self.assertEqual(self.book.status, Book.Status.ACTIVE)

    def test_str_method(self):
        self.assertEqual(str(self.book), "Test Book")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.book.get_absolute_url(),
            reverse("products:book_detail", kwargs={"pk": self.book.pk}),
        )

    def test_max_length_name(self):
        with self.assertRaises(ValidationError):
            test_data = Book(
                category=self.category,
                name="a" * 201,
                author=self.author,
                publisher="test",
                published_at="1999-12-12",
                price=1000,
                description="test",
                stock=5,
                status=Book.Status.ACTIVE,
            )
            test_data.full_clean()

    def test_max_length_publisher(self):
        with self.assertRaises(ValidationError):
            test_data = Book(
                category=self.category,
                name="Test Book",
                author=self.author,
                publisher="a" * 51,
                published_at="1999-12-12",
                price=1000,
                description="test",
                stock=5,
                status=Book.Status.ACTIVE,
            )
            test_data.full_clean()

    def test_blank_description(self):
        test_data = Book(
            category=self.category,
            name="Test Book",
            author=self.author,
            publisher="test",
            published_at="1999-12-12",
            price=1000,
            stock=5,
            status=Book.Status.ACTIVE,
        )
        test_data.full_clean()

    def test_negative_price(self):
        with self.assertRaises(ValidationError):
            test_data = Book(
                category=self.category,
                name="Test Book",
                author=self.author,
                publisher="test",
                published_at="1999-12-12",
                price=-1000,
                description="test",
                stock=5,
                status=Book.Status.ACTIVE,
            )
            test_data.full_clean()

    def test_negative_stock(self):
        with self.assertRaises(ValidationError):
            test_data = Book(
                category=self.category,
                name="Test Book",
                author=self.author,
                publisher="test",
                published_at="1999-12-12",
                price=1000,
                description="test",
                stock=-5,
                status=Book.Status.ACTIVE,
            )
            test_data.full_clean()

    def test_default_status(self):
        test_data = Book(
            category=self.category,
            name="Test Book",
            author=self.author,
            publisher="test",
            published_at="1999-12-12",
            price=1000,
            description="test",
            stock=5,
        )
        test_data.full_clean()
        self.assertEqual(test_data.status, Book.Status.DRAFT)

    def test_invalid_status(self):
        with self.assertRaises(ValidationError):
            test_data = Book(
                category=self.category,
                name="Test Book",
                author=self.author,
                publisher="test",
                published_at="1999-12-12",
                price=1000,
                description="test",
                stock=5,
                status="XX",
            )
            test_data.full_clean()


class FavoriteToggleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testu@test.com", password="testpass"
        )
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.author = Author.objects.create(
            name="Test Author",
            kana_name="テストオーサー",
            birth_date="2000-01-01",
            bio="Test bio",
        )
        self.book = Book.objects.create(
            category=self.category,
            name="Test Book",
            author=self.author,
            publisher="test",
            published_at="1999-12-12",
            price=100,
            description="test",
            stock=1,
            status=Book.Status.ACTIVE,
        )

    # Condition test
    def test_favorite_toggle(self):
        # login
        self.client.force_login(self.user)

        url = reverse("products:favorite_toggle", kwargs={"pk": self.book.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorite.objects.filter(id=self.user.id).exists())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Favorite.objects.filter(id=self.user.id).exists())

    # anonymous user test
    def test_favorite_toggle_login(self):
        url = reverse("products:favorite_toggle", kwargs={"pk": self.book.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
