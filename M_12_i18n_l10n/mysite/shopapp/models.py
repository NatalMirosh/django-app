from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _



def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
        ordering = ["name", "price"]

    name = models.CharField(max_length=100, verbose_name=_('Название'))
    description = models.TextField(null=False, blank=True, verbose_name=_('Описание'))
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_('Цена'))
    discount = models.SmallIntegerField(default=0, verbose_name=_('Скидка'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    archived = models.BooleanField(default=False, verbose_name=_('Архивировано'))
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path, verbose_name=_('Превью'))

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True, verbose_name=_('Описание'))


class Order(models.Model):
    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    delivery_address = models.TextField(null=True, blank=True, verbose_name=_('Адрес доставки'))
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name=_('Промокод'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Пользователь'))
    products = models.ManyToManyField(Product, related_name="orders", verbose_name=_('Товар'))
    receipt = models.FileField(null=True, upload_to='orders/receipts/', verbose_name=_('Квитанция'))
