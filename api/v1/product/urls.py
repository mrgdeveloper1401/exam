from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ProductImageViewSet,
    OrderViewSet,
    OrderItemViewSet
)

app_name = "v1_product"

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename="category")
router.register('products', ProductViewSet, basename="product")
router.register('orders', OrderViewSet, basename="order")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register(r'images', ProductImageViewSet, basename='product-images')

order_router = routers.NestedDefaultRouter(router, "orders", lookup="order")
order_router.register(r'items', OrderItemViewSet, basename='order-items')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_pk>/', include(product_router.urls)),
    path('orders/<int:order_pk>/', include(order_router.urls)),

]