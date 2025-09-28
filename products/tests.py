from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser, Favorite
from products.models import Book, Author, Category

class FavoriteToggleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', email="testu@test.com", password='testpass')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.author = Author.objects.create(name='Test Author', kana_name='テストオーサー', birth_date='2000-01-01', bio='Test bio')
        self.book = Book.objects.create(category=self.category, name='Test Book', author=self.author, publisher="test", published_at="1999-12-12", price=100, description="test", stock=1, status=Book.Status.ACTIVE)


    # Condition test
    def test_favorite_toggle(self):
        # login
        self.client.force_login(self.user)

        url = reverse('products:favorite_toggle', kwargs={"pk": self.book.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorite.objects.filter(id=self.user.id).exists())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Favorite.objects.filter(id=self.user.id).exists())


    # anonymous user test
    def test_favorite_toggle_login(self):
        url = reverse('products:favorite_toggle', kwargs={"pk": self.book.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)