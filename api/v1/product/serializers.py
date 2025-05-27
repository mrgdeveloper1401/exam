from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from products.models import Category, Product, ProductImage, Order, OrderItem, State, City


class CreateCategorySerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = ("name", "parent")

    def create(self, validated_data):
        parent = validated_data.pop("parent", None)

        if parent is None:
            return Category.add_root(**validated_data)
        else:
            category = get_object_or_404(Category, pk=parent)
            return category.add_child(**validated_data)


class CategoryBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
