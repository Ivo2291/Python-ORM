from django.core import validators
from django.db import models

from main_app.validators import validate_menu_categories


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(2, 'Name must be at least 2 characters long.'),
            validators.MaxLengthValidator(100, 'Name cannot exceed 100 characters.'),
        ],
    )

    location = models.CharField(
        max_length=200,
        validators=[
            validators.MinLengthValidator(2, 'Location must be at least 2 characters long.'),
            validators.MaxLengthValidator(200, 'Location cannot exceed 200 characters.'),
        ],
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0, 'Rating must be at least 0.00.'),
            validators.MaxValueValidator(5, 'Rating cannot exceed 5.00.'),
        ],
    )


class Menu(models.Model):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        validators=[
            validate_menu_categories,
        ]
    )

    restaurant = models.ForeignKey(
        to='Restaurant',
        on_delete=models.CASCADE,
    )
