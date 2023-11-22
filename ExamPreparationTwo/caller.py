import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile


# print(Profile.objects.get_regular_customers())


def get_profiles(search_string=None):
    if search_string is None:
        return ''

    query = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(
        phone_number__icontains=search_string)

    searched_profiles = Profile.objects.annotate(orders_count=Count('orders')).filter(query).order_by('full_name')

    if not searched_profiles:
        return ''

    return '\n'.join([f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, "
                      f"orders: {p.orders_count}" for p in searched_profiles])


# print(get_profiles('gmail'))
