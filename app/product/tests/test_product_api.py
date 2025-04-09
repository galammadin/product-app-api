"""
Tests for product APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Product,
    Tag,
    Category,
)

from product.serializers import (
    ProductSerializer,
    ProductDetailSerializer,
)


PRODUCTS_URL = reverse('product:product-list')


def detail_url(product_id):
    """Create and return a product detail URL."""
    return reverse('product:product-detail', args=[product_id])


def create_product(user, **params):
    """Create and return a sample product."""
    defaults = {
        'title': 'Sample product title',
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/product.pdf',
    }
    defaults.update(params)

    product = Product.objects.create(user=user, **defaults)
    return product


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicProductAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving a list of products."""
        create_product(user=self.user)
        create_product(user=self.user)

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_product_list_limited_to_user(self):
        """Test list of products is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_product(user=other_user)
        create_product(user=self.user)

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.filter(user=self.user)
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_product_detail(self):
        """Test get product detail."""
        product = create_product(user=self.user)

        url = detail_url(product.id)
        res = self.client.get(url)

        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.data, serializer.data)

    def test_create_product(self):
        """Test creating a product."""
        payload = {
            'title': 'Sample product',
            'price': Decimal('5.99'),
        }
        res = self.client.post(PRODUCTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)
        self.assertEqual(product.user, self.user)

    def test_partial_update(self):
        """Test partial update of a product."""
        original_link = 'https://example.com/product.pdf'
        product = create_product(
            user=self.user,
            title='Sample product title',
            link=original_link,
        )

        payload = {'title': 'New product title'}
        url = detail_url(product.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.title, payload['title'])
        self.assertEqual(product.link, original_link)
        self.assertEqual(product.user, self.user)

    def test_full_update(self):
        """Test full update of product."""
        product = create_product(
            user=self.user,
            title='Sample product title',
            link='https://exmaple.com/product.pdf',
            description='Sample product description.',
        )

        payload = {
            'title': 'New product title',
            'link': 'https://example.com/new-product.pdf',
            'description': 'New product description',
            'price': Decimal('2.50'),
        }
        url = detail_url(product.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)
        self.assertEqual(product.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the product user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        product = create_product(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(product.id)
        self.client.patch(url, payload)

        product.refresh_from_db()
        self.assertEqual(product.user, self.user)

    def test_delete_product(self):
        """Test deleting a product successful."""
        product = create_product(user=self.user)

        url = detail_url(product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())

    def test_product_other_users_product_error(self):
        """Test trying to delete another users product gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        product = create_product(user=new_user)

        url = detail_url(product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Product.objects.filter(id=product.id).exists())

    def test_create_product_with_new_tags(self):
        """Test creating a product with new tags."""
        payload = {
            'title': 'Fork',
            'time_minutes': 30,
            'price': Decimal('2.50'),
            'tags': [{'name': 'Kitchen'}, {'name': 'Tool'}],
        }
        res = self.client.post(PRODUCTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        products = Product.objects.filter(user=self.user)
        self.assertEqual(products.count(), 1)
        product = products[0]
        self.assertEqual(product.tags.count(), 2)
        for tag in payload['tags']:
            exists = product.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_product_with_existing_tags(self):
        """Test creating a product with existing tag."""
        tag_indian = Tag.objects.create(user=self.user, name='Kitchen')
        payload = {
            'title': 'Knife',
            'time_minutes': 60,
            'price': Decimal('4.50'),
            'tags': [{'name': 'Kitchen'}, {'name': 'Dangerous'}],
        }
        res = self.client.post(PRODUCTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        products = Product.objects.filter(user=self.user)
        self.assertEqual(products.count(), 1)
        product = products[0]
        self.assertEqual(product.tags.count(), 2)
        self.assertIn(tag_indian, product.tags.all())
        for tag in payload['tags']:
            exists = product.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """Test create tag when updating a product."""
        product = create_product(user=self.user)

        payload = {'tags': [{'name': 'Baseball'}]}
        url = detail_url(product.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='Baseball')
        self.assertIn(new_tag, product.tags.all())

    def test_update_product_assign_tag(self):
        """Test assigning an existing tag when updating a product."""
        tag_kitchen = Tag.objects.create(user=self.user, name='Kitchen')
        product = create_product(user=self.user)
        product.tags.add(tag_kitchen)

        tag_sports = Tag.objects.create(user=self.user, name='Sports')
        payload = {'tags': [{'name': 'Sports'}]}
        url = detail_url(product.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_sports, product.tags.all())
        self.assertNotIn(tag_kitchen, product.tags.all())

    def test_clear_product_tags(self):
        """Test clearing a products tags."""
        tag = Tag.objects.create(user=self.user, name='Kitchen')
        product = create_product(user=self.user)
        product.tags.add(tag)

        payload = {'tags': []}
        url = detail_url(product.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(product.tags.count(), 0)

    def test_filter_products_by_tags(self):
        """Test filtering products by tags."""
        tag1 = Tag.objects.create(user=self.user, name='Electronics')
        tag2 = Tag.objects.create(user=self.user, name='Clothing')

        product1 = create_product(user=self.user, title='Laptop')
        product1.tags.add(tag1)

        product2 = create_product(user=self.user, title='T-shirt')
        product2.tags.add(tag2)

        res = self.client.get(PRODUCTS_URL, {'tags': tag1.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'Laptop')

    def test_filter_products_by_category(self):
        """Test filtering products by category."""
        category1 = Category.objects.create(user=self.user, name='Electronics')
        category2 = Category.objects.create(user=self.user, name='Clothing')

        product1 = create_product(user=self.user, title='Laptop')
        product1.category = category1
        product1.save()

        product2 = create_product(user=self.user, title='T-shirt')
        product2.category = category2
        product2.save()

        res = self.client.get(PRODUCTS_URL, {'category': category1.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'Laptop')

    def test_search_products(self):
        """Test searching products."""
        create_product(user=self.user, title='Laptop', description='High-end laptop')
        create_product(user=self.user, title='T-shirt', description='Cotton t-shirt')

        res = self.client.get(PRODUCTS_URL, {'search': 'laptop'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'Laptop')

    def test_order_products(self):
        """Test ordering products."""
        create_product(user=self.user, title='Zebra', price=Decimal('10.00'))
        create_product(user=self.user, title='Apple', price=Decimal('5.00'))

        res = self.client.get(PRODUCTS_URL, {'ordering': 'title'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['title'], 'Apple')
        self.assertEqual(res.data[1]['title'], 'Zebra')
