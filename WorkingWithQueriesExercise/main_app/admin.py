from django.contrib import admin

from main_app.models import Laptop


# Register your models here.
@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    pass
