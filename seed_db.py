import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grodiur.settings')
django.setup()

from products.models import Category

def seed():
    categories = [
        {'name': 'Vegetables', 'slug': 'vegetables'},
        {'name': 'Fruits', 'slug': 'fruits'},
        {'name': 'Dairy & Eggs', 'slug': 'dairy-eggs'},
        {'name': 'Rice & Grains', 'slug': 'rice-grains'},
        {'name': 'Masala & Spices', 'slug': 'masala-spices'}
    ]
    
    for cat in categories:
        Category.objects.get_or_create(slug=cat['slug'], defaults={'name': cat['name']})
    print("Database seeded with default categories successfully.")

if __name__ == '__main__':
    seed()
