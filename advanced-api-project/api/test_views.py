from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.author = Author.objects.create(name='George Orwell')
        self.book = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author
        )

    def test_list_books_unauthenticated(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_book(self):
        response = self.client.get(f'/api/books/{self.book.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')

    def test_create_book_unauthenticated(self):
        data = {'title': 'Animal Farm', 'publication_year': 1945, 'author': self.author.pk}
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'title': 'Animal Farm', 'publication_year': 1945, 'author': self.author.pk}
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'title': 'Nineteen Eighty-Four', 'publication_year': 1949, 'author': self.author.pk}
        response = self.client.put(f'/api/books/{self.book.pk}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(f'/api/books/{self.book.pk}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_books(self):
        response = self.client.get('/api/books/?title=1984')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self):
        response = self.client.get('/api/books/?search=Orwell')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_books(self):
        response = self.client.get('/api/books/?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_publication_year(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'title': 'Future Book', 'publication_year': 9999, 'author': self.author.pk}
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
