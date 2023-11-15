from django.core.exceptions import ValidationError


def video_game_rating_validator(value):
    if not 0.0 <= value <= 10.0:
        raise ValidationError('The rating must be between 0.0 and 10.0')


def video_game_release_year_validator(value):
    if not 1990 <= value <= 2023:
        raise ValidationError('The release year must be between 1990 and 2023')
