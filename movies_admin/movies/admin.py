from django.contrib import admin
from .models import Filmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    pass 
