from django.core import validators
from django.db import models

from main_app.mixins import PersonInfo, AwardedInfo, LastUpdate


class Director(PersonInfo):
    years_of_experience = models.SmallIntegerField(
        validators=[
            validators.MinValueValidator(0),
        ],
        default=0,
    )


class Actor(PersonInfo, AwardedInfo, LastUpdate):
    pass


class Movie(AwardedInfo, LastUpdate):
    ACTION = 'Action'
    COMEDY = 'Comedy'
    DRAMA = 'Drama'
    OTHER = 'Other'

    GENRE_CHOICES = [
        (ACTION, 'Action'),
        (COMEDY, 'Comedy'),
        (DRAMA, 'Drama'),
        (OTHER, 'Other'),
    ]

    title = models.CharField(
        max_length=150,
        validators=[
            validators.MinLengthValidator(5),
        ],
    )

    release_date = models.DateField()

    storyline = models.TextField(
        blank=True,
        null=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=GENRE_CHOICES,
        default=OTHER,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            validators.MinValueValidator(0.0),
            validators.MaxValueValidator(10.0),
        ],
        default=0.0
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        to='Director',
        on_delete=models.CASCADE,
        related_name='movies',
    )

    starring_actor = models.ForeignKey(
        to='Actor',
        on_delete=models.SET_NULL,
        related_name='starring_movies',
        blank=True,
        null=True,
    )

    actors = models.ManyToManyField(
        to='Actor',
        related_name='movies',
    )
