from django.core import validators
from django.db import models


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            validators.RegexValidator(
                '[a-zA-Z\s]+$', message='Name can only contain letters and spaces'
            ),
        ]
    )

    age = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(18, message='Age must be greater than 18')
        ]
    )

    email = models.EmailField(
        error_messages={'invalid': 'Enter a valid email address'}
    )

    phone_number = models.CharField(
        max_length=13,
        validators=[
            validators.RegexValidator(
                '^\+359[0-9]{9}$', message="Phone number must start with a '+359' followed by 9 digits"
            ),
        ],
    )

    website_url = models.URLField(
        error_messages={'invalid': 'Enter a valid URL'}
    )
