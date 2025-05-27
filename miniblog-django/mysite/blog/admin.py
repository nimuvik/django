from django.contrib import admin
from django.utils import timezone
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']
    # убираем readonly, чтобы цена сохранялась
    # можно вернуть, если хочешь, чтобы поле было только для чтения
    # readonly_fields = ['price']


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    readonly_fields = ['payment_date']


@admin.register(Product)  # товары
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'stock', 'category', 'expiry_status')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'description', 'brand')
    list_display_links = ('name', 'brand')

    @admin.display(description="Статус срока")
    def expiry_status(self, obj):
        if obj.expiry_date:
            return "Срок годности" if obj.expiry_date > timezone.now().date() else "Просрочено"
        return "Нет данных"


@admin.register(Order)  # заказы
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at', 'payment_status')
    list_filter = ('status', 'created_at', 'delivery_method')
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline, PaymentInline]
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'user')
    raw_id_fields = ['user']

    @admin.display(description="Статус оплаты")
    def payment_status(self, obj):
        payments = obj.payment_set.all()
        if not payments:
            return "Не оплачен"
        return ", ".join([p.get_status_display() for p in payments])

    # вот добавленный метод, который автоматически подставляет цену
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, OrderItem):
                if not instance.price:
                    instance.price = instance.product.price
            instance.save()
        formset.save_m2m()


@admin.register(Review)  # отзывы
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at', 'short_comment')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    date_hierarchy = 'created_at'

    @admin.display(description="Комментарий")
    def short_comment(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment


@admin.register(Category)  # категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')

    @admin.display(description="Товаров")
    def product_count(self, obj):
        return obj.product_set.count()


@admin.register(Favorite)  # избранное
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'product')


# обычная регистрация остальных моделей
admin.site.register(DeliveryMethod)
admin.site.register(Payment)
admin.site.register(Promotion)
