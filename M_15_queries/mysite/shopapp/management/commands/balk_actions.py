# from django.contrib.auth.models import User
#
# from django.core.management import BaseCommand
#
# from shopapp.models import Product
#
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         self.stdout.write("Start demo bulk_action")
#
#         result = Product.objects.filter(
#             name__contains="Smartphone",
#         ).update(discount=10)
#
#         print(result)
#
#         # info = [
#         #     ('smartphone 1', 199),
#         #     ('smartphone 2', 299),
#         #     ('smartphone 3', 399),
#         # ]
#         # products = [
#         #     Product(name=name, price=price)
#         #     for name, price in info
#         # ]
#         # result = Product.objects.bulk_create(products)
#         #
#         # for obj in result:
#         #     print(obj)
#
#         self.stdout.write(f"Done")
