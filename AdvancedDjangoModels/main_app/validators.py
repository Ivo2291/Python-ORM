from django.core.exceptions import ValidationError


def validate_menu_categories(value):
    valid_categories = ["Appetizers", "Main Course", "Desserts"]

    if not all([category for category in valid_categories if category.lower() in value.lower()]):
        raise ValidationError(
            'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".'
        )
