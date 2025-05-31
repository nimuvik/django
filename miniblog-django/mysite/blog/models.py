from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название метода")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Метод доставки"
        verbose_name_plural = "Методы доставки"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="Количество на складе")
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    expiry_date = models.DateField(verbose_name="Срок годности", null=True, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.brand})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.SET_NULL, null=True, verbose_name="Метод доставки")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product.name} x{self.quantity} в заказе #{self.order.id}"

class Payment(models.Model):
    METHOD_CHOICES = [
        ('card', 'Карта'),
        ('cash', 'Наличные'),
        ('transfer', 'Перевод'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершен'),
        ('failed', 'Ошибка'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    payment_date = models.DateTimeField(default=timezone.now, verbose_name="Дата платежа")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, verbose_name="Метод оплаты")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж #{self.id} для заказа #{self.order.id}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"

class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    description = models.TextField(verbose_name="Описание акции")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return f"Акция на {self.product.name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные товары"
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.name} в избранном у {self.user.username}"


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]

    title = models.CharField(max_length=250, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    body = models.TextField(verbose_name="Текст статьи")
    publish = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ('-publish',)

    def __str__(self):
        return self.title
