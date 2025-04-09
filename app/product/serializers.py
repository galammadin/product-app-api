"""
Serializers for product APIs
"""
from rest_framework import serializers

from core.models import (
    Product,
    Tag,
    Category,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories."""

    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products."""
    tags = TagSerializer(many=True, required=False)
    category = CategorySerializer(required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'link', 'tags', 'category']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, product):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            product.tags.add(tag_obj)

    def _get_or_create_category(self, category_data, product):
        """Handle getting or creating category as needed."""
        auth_user = self.context['request'].user
        if category_data:
            category_obj, created = Category.objects.get_or_create(
                user=auth_user,
                **category_data,
            )
            product.category = category_obj
            product.save()

    def create(self, validated_data):
        """Create a product."""
        tags = validated_data.pop('tags', [])
        category = validated_data.pop('category', None)
        product = Product.objects.create(**validated_data)
        self._get_or_create_tags(tags, product)
        self._get_or_create_category(category, product)

        return product

    def update(self, instance, validated_data):
        """Update product."""
        tags = validated_data.pop('tags', None)
        category = validated_data.pop('category', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if category is not None:
            self._get_or_create_category(category, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProductDetailSerializer(ProductSerializer):
    """Serializer for product detail view."""

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description']
