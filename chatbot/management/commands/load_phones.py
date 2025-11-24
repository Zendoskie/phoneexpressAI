from django.core.management.base import BaseCommand
from chatbot.models import Phone


class Command(BaseCommand):
    help = 'Loads initial phone data into the database'

    def handle(self, *args, **options):
        phones_data = [
            {
                'name': 'iPhone 15 Pro Max',
                'brand': 'Apple',
                'model': 'iPhone 15 Pro Max',
                'price_php': 89900.00,
                'description': '6.7-inch Super Retina XDR display, A17 Pro chip, 48MP Main camera, Titanium design',
                'stock': 15,
            },
            {
                'name': 'iPhone 15',
                'brand': 'Apple',
                'model': 'iPhone 15',
                'price_php': 64900.00,
                'description': '6.1-inch Super Retina XDR display, A16 Bionic chip, 48MP Main camera',
                'stock': 20,
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'brand': 'Samsung',
                'model': 'Galaxy S24 Ultra',
                'price_php': 84990.00,
                'description': '6.8-inch Dynamic AMOLED 2X, Snapdragon 8 Gen 3, 200MP camera, S Pen included',
                'stock': 12,
            },
            {
                'name': 'Samsung Galaxy S24',
                'brand': 'Samsung',
                'model': 'Galaxy S24',
                'price_php': 54990.00,
                'description': '6.2-inch Dynamic AMOLED 2X, Snapdragon 8 Gen 3, 50MP camera',
                'stock': 18,
            },
            {
                'name': 'OnePlus 12',
                'brand': 'OnePlus',
                'model': 'OnePlus 12',
                'price_php': 45990.00,
                'description': '6.82-inch LTPO OLED, Snapdragon 8 Gen 3, 50MP main camera, 100W fast charging',
                'stock': 10,
            },
            {
                'name': 'Xiaomi 14 Pro',
                'brand': 'Xiaomi',
                'model': 'Xiaomi 14 Pro',
                'price_php': 39990.00,
                'description': '6.73-inch LTPO AMOLED, Snapdragon 8 Gen 3, 50MP Leica triple camera',
                'stock': 14,
            },
            {
                'name': 'Google Pixel 8 Pro',
                'brand': 'Google',
                'model': 'Pixel 8 Pro',
                'price_php': 54990.00,
                'description': '6.7-inch LTPO OLED, Google Tensor G3, 50MP main camera, AI-powered features',
                'stock': 8,
            },
            {
                'name': 'Huawei P60 Pro',
                'brand': 'Huawei',
                'model': 'P60 Pro',
                'price_php': 49990.00,
                'description': '6.67-inch LTPO OLED, Snapdragon 8+ Gen 1, 48MP main camera',
                'stock': 6,
            },
            {
                'name': 'Realme GT 5 Pro',
                'brand': 'Realme',
                'model': 'GT 5 Pro',
                'price_php': 34990.00,
                'description': '6.78-inch AMOLED, Snapdragon 8 Gen 3, 50MP main camera, 5400mAh battery',
                'stock': 16,
            },
            {
                'name': 'OPPO Find X6 Pro',
                'brand': 'OPPO',
                'model': 'Find X6 Pro',
                'price_php': 44990.00,
                'description': '6.82-inch LTPO AMOLED, Snapdragon 8 Gen 2, 50MP triple camera system',
                'stock': 9,
            },
        ]

        created_count = 0
        updated_count = 0

        for phone_data in phones_data:
            phone, created = Phone.objects.update_or_create(
                brand=phone_data['brand'],
                model=phone_data['model'],
                defaults=phone_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {phone.brand} {phone.model}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated: {phone.brand} {phone.model}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully loaded phones: {created_count} created, {updated_count} updated'
            )
        )

