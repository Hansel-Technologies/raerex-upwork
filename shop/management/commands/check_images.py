# management/commands/check_images.py
from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Check and report on product images in the database'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            if product.image:
                self.stdout.write(self.style.SUCCESS(f"Product {product.id}: {product.name}"))
                self.stdout.write(f"  Image size: {len(product.image)} bytes")
                self.stdout.write(f"  Image name: {product.image_name}")
                if len(product.image) < 100:
                    self.stdout.write(self.style.WARNING("  Image data seems too small!"))
            else:
                self.stdout.write(self.style.WARNING(f"Product {product.id}: {product.name} - No image"))