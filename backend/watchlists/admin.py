from django.contrib import admin
from .models import Watchlists

class WatchlistsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_dt', )
    
admin.site.register(Watchlists, WatchlistsAdmin)