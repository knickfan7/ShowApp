from rest_framework import serializers

from .models import Watchlists

class WatchlistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Watchlists
        fields = ['id', 'name', 'owner', 'show', 'description', 'created_dt']