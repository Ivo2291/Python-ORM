import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location


# 01. Pet task

def create_pet(name: str, species: str):
    Pet.objects.create(name=name, species=species)

    return f"{name} is a very cute {species}!"


# 02. Artifact task

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artefact_to_create = Artifact(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )

    artefact_to_create.save()

    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts():
    Artifact.objects.all().delete()


# 03. Locations task

# def make_new_location(name: str, region: str, population: int, description: str, is_capital: bool):
#     Location.objects.create(
#         name=name,
#         region=region,
#         population=population,
#         description=description,
#         is_capital=is_capital,
#     )


def show_all_locations():
    locations_list = []

    all_locations = Location.objects.all().order_by('-id')

    for location in all_locations:
        locations_list.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(locations_list)


def new_capital():
    location = Location.objects.first()

    location.is_capital = True

    location.save()


def get_capitals():
    location = Location.objects.all().filter(is_capital=True).values('name')

    return location


def delete_first_location():
    Location.objects.first().delete()


# 04. Car task

