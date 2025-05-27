from django.db import models
from treebeard.mp_tree import MP_Node

from core.models import ModifyMixin


class Category(MP_Node, ModifyMixin):
    name = models.CharField(max_length=100, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='اسلاگ')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    node_order_by = ['name']

    class Meta:
        db_table = 'category'
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name


class Product(ModifyMixin):
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='دسته‌بندی')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         verbose_name='قیمت با تخفیف')
    stock = models.PositiveIntegerField(verbose_name='موجودی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']
        db_table = 'product'

    def __str__(self):
        return self.name

    # @property
    # def has_discount(self):
    #     return self.discount_price is not None and self.discount_price < self.price


class ProductImage(ModifyMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', verbose_name='تصویر')
    is_main = models.BooleanField(default=False, verbose_name='تصویر اصلی')

    class Meta:
        db_table = 'product_image'
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'


class State(ModifyMixin):
    name = models.CharField(max_length=50, verbose_name='نام استان')

    class Meta:
        db_table = 'state'
        verbose_name = 'استان'
        verbose_name_plural = 'استان‌ها'

    def __str__(self):
        return self.name


class City(ModifyMixin):
    name = models.CharField(max_length=50, verbose_name='نام شهر')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities', verbose_name='استان')

    class Meta:
        db_table = 'city'
        verbose_name = 'شهر'
        verbose_name_plural = 'شهرها'

    def __str__(self):
        return f"{self.name} - {self.state.name}"


class Order(ModifyMixin):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    )

    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT, related_name='orders', verbose_name='کاربر')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='مبلغ کل')
    shipping_address = models.TextField(verbose_name='آدرس ارسال')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='شهر')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تماس')

    class Meta:
        db_table = 'order'
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش #{self.id} - {self.user.phone_number}"


class OrderItem(ModifyMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='محصول')
    quantity = models.PositiveIntegerField(verbose_name='تعداد')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت واحد')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.price
