import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student


def add_students():
    students = [
        {
            'student_id': 'FC5204',
            'first_name': 'John',
            'last_name': 'Doe',
            'birth_date': date(1995, 5, 15),
            'email': 'john.doe@university.com',
        },
        {
            'student_id': 'FE0054',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'birth_date': None,
            'email': 'jane.smith@university.com',
        },
        {
            'student_id': 'FH2014',
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'birth_date': date(1998, 2, 10),
            'email': 'alice.johnson@university.com',
        },
        {
            'student_id': 'FH2015',
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'birth_date': date(1996, 11, 25),
            'email': 'bob.wilson@university.com',
        },
    ]

    for student in students:
        Student.objects.create(**student)


def get_students_info():
    students_info = []

    students = Student.objects.all()

    for student in students:
        students_info.append(
            f"Student №{student.student_id}: {student.first_name} "
            f"{student.last_name}; Email: {student.email}"
        )

    return '\n'.join(students_info)


def update_students_emails():
    students = Student.objects.all()

    for student in students:
        updated_email = student.email.replace('university', 'uni-students')
        student.email = updated_email
        student.save()


def truncate_students():
    Student.objects.all().delete()
