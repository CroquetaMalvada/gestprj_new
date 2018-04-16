from django.contrib import admin
from gestprj.models import Projectes

admin.site.register(Projectes)

# Register your models here.

# admin.site.register() + CREAR USUARIO ADMIN con el python manage.py craetesuperuser