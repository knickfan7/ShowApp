from django.contrib import admin
from .models import Shows
# Register your models here.

class ShowsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shows, ShowsAdmin)