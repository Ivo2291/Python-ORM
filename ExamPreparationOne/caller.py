import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor
from django.db.models import Q, Count, Avg


# print(Director.objects.get_directors_by_movies_count())

def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    directors_by_name = Q(full_name__icontains=search_name)
    directors_by_nationality = Q(nationality__icontains=search_nationality)

    if search_name and search_nationality:
        query = Q(directors_by_name & directors_by_nationality)
    elif not search_name:
        query = Q(directors_by_nationality)
    else:
        query = Q(directors_by_name)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = [
        f"Director: {director.full_name}, nationality: {director.nationality}, "
        f"experience: {director.years_of_experience}" for director in directors
    ]

    return '\n'.join(result)


# print(get_directors(search_name=None, search_nationality='ital'))

def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."


# print(get_top_director())

def get_top_actor():
    top_actor = Actor.objects.prefetch_related('starring_movies')\
        .annotate(starring_movies_count=Count('starring_movies'), avg_rating=Avg('starring_movies__rating'))\
        .order_by('-starring_movies_count', 'full_name')\
        .first()

    if not top_actor or not top_actor.starring_movies_count:
        return ''

    movies = ', '.join([movie.title for movie in top_actor.starring_movies.all()])

    return f"Top Actor: {top_actor.full_name}, starring in movies: {movies}, " \
           f"movies average rating: {top_actor.avg_rating:.1f}"


# print(get_top_actor())
