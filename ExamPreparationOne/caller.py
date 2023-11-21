import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
from django.db.models import Q, F, Count, Avg, Max


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
    top_actor = Actor.objects.prefetch_related('starring_movies') \
        .annotate(starring_movies_count=Count('starring_movies'), avg_rating=Avg('starring_movies__rating')) \
        .order_by('-starring_movies_count', 'full_name') \
        .first()

    if not top_actor or not top_actor.starring_movies_count:
        return ''

    movies = ', '.join([movie.title for movie in top_actor.starring_movies.all()])

    return f"Top Actor: {top_actor.full_name}, starring in movies: {movies}, " \
           f"movies average rating: {top_actor.avg_rating:.1f}"


# print(get_top_actor())


def get_actors_by_movies_count():
    if Movie.objects.all().count() == 0:
        return ''

    top_three_actors = Actor.objects.prefetch_related('movies') \
                           .annotate(movies_count=Count('movies')) \
                           .order_by('-movies_count', 'full_name')[:3]

    if not top_three_actors:
        return ''

    result = [f"{actor.full_name}, participated in {actor.movies_count} movies" for actor in top_three_actors]

    return '\n'.join(result)


# print(get_actors_by_movies_count())

def get_top_rated_awarded_movie():
    top_movie = Movie.objects.select_related('starring_actor') \
        .prefetch_related('actors') \
        .filter(is_awarded=True) \
        .order_by('-rating', 'title') \
        .first()

    if not top_movie:
        return ''

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    cast = ', '.join([actor.full_name for actor in top_movie.actors.all().order_by('full_name')])

    return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. " \
           f"Starring actor: {starring_actor}. Cast: {cast}."


# print(get_top_rated_awarded_movie())


def increase_rating():
    updated_movies = Movie.objects.filter(rating__lt=10.0, is_classic=True).update(rating=F('rating') + 0.1)

    if updated_movies == 0:
        return f"No ratings increased."

    return f"Rating increased for {updated_movies} movies."

# print(increase_rating())