from rest_framework import viewsets, generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .serializers import (
    CreateCategorySerializer,
    CategoryBlogSerializer,
    ProductSerializer,
    ProductImageSerializer,
    OrderSerializer,
    OrderItemSerializer
)
from products.models import Category, Product, ProductImage, Order, OrderItem


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateCategorySerializer
        return CategoryBlogSerializer

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category').prefetch_related('images')
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs['product_pk'])

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().prefetch_related('items')
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        items_data = request.data.get('items', [])
        for item_data in items_data:
            product = get_object_or_404(Product, pk=item_data['product'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )

        return Response(serializer.data, status=201)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs['order_pk'])