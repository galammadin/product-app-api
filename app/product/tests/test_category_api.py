"""
Tests for the categories API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

from product.serializers import CategorySerializer


CATEGORIES_URL = reverse('product:category-list')


def detail_url(category_id):
    """Create and return a category detail url."""
    return reverse('product:category-detail', args=[category_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicCategoriesApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving categories."""
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoriesApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_categories(self):
        """Test retrieving a list of categories."""
        Category.objects.create(user=self.user, name='Electronics')
        Category.objects.create(user=self.user, name='Clothing')

        res = self.client.get(CATEGORIES_URL)

        categories = Category.objects.all().order_by('-name')
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_categories_limited_to_user(self):
        """Test list of categories is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Category.objects.create(user=user2, name='Food')
        category = Category.objects.create(user=self.user, name='Electronics')

        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], category.name)
        self.assertEqual(res.data[0]['id'], category.id)

    def test_update_category(self):
        """Test updating a category."""
        category = Category.objects.create(user=self.user, name='Electronics')

        payload = {'name': 'Gadgets'}
        url = detail_url(category.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, payload['name'])

    def test_delete_category(self):
        """Test deleting a category."""
        category = Category.objects.create(user=self.user, name='Electronics')

        url = detail_url(category.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        categories = Category.objects.filter(user=self.user)
        self.assertFalse(categories.exists())
