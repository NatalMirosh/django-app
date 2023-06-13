from django.core.management import BaseCommand

from shopapp.models import Product

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products_names = [
            "Laptop",
            "Desktop",
            "Smartphone",
        ]
        for products_name in products_names:
            product, created = Product.objects.get_or_create(name=products_name)
            self.stdout.write(f"Created product {product.name}")
            logger.info(f"Products created {products_name}")

        logger.info("Products created")
        self.stdout.write(self.style.SUCCESS("Products created"))
