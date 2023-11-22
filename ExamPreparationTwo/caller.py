import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Order, Product


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


def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()

    return '\n'.join([f"Profile: {p.full_name}, orders: {p.orders_count}" for p in loyal_profiles])

# print(get_loyal_profiles())


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if not last_order or not last_order.products.all():
        return ''

    products = ', '.join([p.name for p in last_order.products.all().order_by('name')])

    return f"Last sold products: {products}"

# print(get_last_sold_products())


def get_top_products():
    top_products = Product.objects.annotate(
        orders_count=Count('order')
    ).filter(
        orders_count__gt=0
    ).order_by(
        '-orders_count',
        'name',
    )[:5]

    if not top_products:
        return ''

    products = [f"{p.name}, sold {p.orders_count} times" for p in top_products]

    return f"Top products:\n" + '\n'.join(products)

# print(get_top_products())


def apply_discounts():
    orders_with_discount = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        is_completed=False,
        products_count__gt=2,
    ).update(
        total_price=F('total_price') * 0.9
    )

    return f"Discount applied to {orders_with_discount} orders."


# print(apply_discounts())


def complete_order():
    oldest_order = Order.objects.prefetch_related(
        'products'
    ).filter(
        is_completed=False
    ).first()

    if not oldest_order:
        return ''

    for product in oldest_order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    oldest_order.is_completed = True
    oldest_order.save()

    return f"Order has been completed!"


# print(complete_order())
