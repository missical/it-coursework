from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from products.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Sets up initial demo data for the marketplace'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up demo data...')
        
        # Create categories
        categories = [
            'Electronics',
            'Clothing',
            'Furniture',
            'Books',
            'Sports',
            'Toys',
            'Home & Garden',
            'Vehicles',
            'Collectibles',
            'Other'
        ]
        
        for category_name in categories:
            Category.objects.get_or_create(
                name=category_name,
                slug=slugify(category_name),
                defaults={'description': f'All kinds of {category_name.lower()} items'}
            )
            self.stdout.write(f'Created category: {category_name}')
        
        # Create a demo user if it doesn't exist
        demo_user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'is_active': True
            }
        )
        
        if created:
            demo_user.set_password('demo1234')
            demo_user.save()
            self.stdout.write('Created demo user: demo_user (password: demo1234)')
        
        # Create some demo products
        if Product.objects.count() == 0:
            electronics = Category.objects.get(name='Electronics')
            furniture = Category.objects.get(name='Furniture')
            books = Category.objects.get(name='Books')
            
            products = [
                {
                    'title': 'Used iPhone 12',
                    'description': 'Used iPhone 12 in good condition. 128GB storage, black color.',
                    'price': 499.99,
                    'category': electronics,
                    'condition': 'Good',
                    'location': 'New York, NY'
                },
                {
                    'title': 'Wooden Dining Table',
                    'description': 'Solid wood dining table with 6 chairs. Minor scratches but overall in good condition.',
                    'price': 299.99,
                    'category': furniture,
                    'condition': 'Good',
                    'location': 'Los Angeles, CA'
                },
                {
                    'title': 'Harry Potter Book Collection',
                    'description': 'Complete set of Harry Potter books (7 books). Paperback edition.',
                    'price': 49.99,
                    'category': books,
                    'condition': 'Like New',
                    'location': 'Chicago, IL'
                }
            ]
            
            for product_data in products:
                product = Product.objects.create(
                    title=product_data['title'],
                    description=product_data['description'],
                    price=product_data['price'],
                    category=product_data['category'],
                    seller=demo_user,
                    condition=product_data['condition'],
                    location=product_data['location'],
                    status='available'
                )
                self.stdout.write(f'Created product: {product.title}')
        
        self.stdout.write(self.style.SUCCESS('Demo data setup complete!')) 