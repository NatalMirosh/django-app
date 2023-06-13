import logging

from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Order, Product

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with products")
        logger.info("Create order with products")

        user = User.objects.get(username="admin")
        products: Sequence[Product] = Product.objects.defer("description", "price", "created_at").all()
        order, created = Order.objects.get_or_create(
            delivery_address="ul Belova, d 8",
            promocode="555",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Created order {order}")
        logger.info(f"Created order {order}")

