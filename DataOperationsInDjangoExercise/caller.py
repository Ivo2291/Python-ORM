import os
from datetime import datetime

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom


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
#         is_capital=is_capital
#     )


def show_all_locations():
    locations_list = []

    all_locations = Location.objects.all().order_by('-id')

    for location in all_locations:
        locations_list.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(locations_list)


def new_capital():
    # Location.objects.filter(pk=1).update(is_capital=True) --> Faster solution

    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals():
    location = Location.objects.all().filter(is_capital=True).values('name')

    return location


def delete_first_location():
    Location.objects.first().delete()


# 04. Car task
# def add_car(model: str, year: int, color: str, price: float):
#     Car.objects.create(
#         model=model,
#         year=year,
#         color=color,
#         price=price
#     )
def apply_discount():
    cars = Car.objects.all()

    for car in cars:
        percentage_of_discount = sum(int(digit) for digit in str(car.year)) / 100
        car_price = float(car.price)
        car.price_with_discount = car_price - car_price * percentage_of_discount
        car.save()


def get_recent_cars():
    recent_cars = Car.objects.all().filter(year__gte=2020).values('model', 'price_with_discount')

    return recent_cars


def delete_last_car():
    Car.objects.last().delete()


# 05. Task task
def add_new_task(title: str, description: str, due_date: str):
    Task.objects.create(
        title=title,
        description=description,
        due_date=due_date
    )


def show_unfinished_tasks():
    # tasks_list = []

    unfinished_tasks = Task.objects.all().filter(is_finished=False)

    # this is without __str__ method in the model:
    # for task in unfinished_tasks:
    #     tasks_list.append(f"Task - {task.title} needs to be done until {task.due_date}!")

    return '\n'.join(str(t) for t in unfinished_tasks)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 != 0 and not task.is_finished:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    encoded_text = ''.join(chr(ord(char) - 3) for char in text)

    Task.objects.all().filter(title=task_title).update(description=encoded_text)


# 06. Hotel Room task
def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    deluxe_rooms_list = []

    for room in deluxe_rooms:
        if room.id % 2 == 0:
            deluxe_rooms_list.append(
                str(room)
            )

    return '\n'.join(deluxe_rooms_list)


def increase_room_capacity():
    rooms = HotelRoom.objects.all()

    for i in range(len(rooms)):
        if not rooms[i].is_reserved:
            continue
        if len(rooms) == 1 or i == 0:
            rooms[i].capacity += rooms[i].id
        else:
            rooms[i].capacity += rooms[i - 1].capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    first_room = HotelRoom.objects.first()

    if not first_room.is_reserved:
        first_room.is_reserved = True
        first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()

    if last_room.is_reserved:
        last_room.delete()
