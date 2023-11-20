from django.core import validators
from django.db import models


class PersonInfo(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[
            validators.MinLengthValidator(2),
        ],
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )

    def __str__(self):
        return f"Name: {self.full_name}"


class AwardedInfo(models.Model):
    class Meta:
        abstract = True

    is_awarded = models.BooleanField(
        default=False,
    )


class LastUpdate(models.Model):
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(
        auto_now=True,
    )
