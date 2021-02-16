from rest_framework import serializers

from .models import Watchlists

class WatchlistSerializers(serializers.ModelSerializer):
    show_id = serializers.IntegerField(source="show.id", read_only=True)
    img = serializers.CharField(source="show.image", read_only=True)
    title = serializers.CharField(source="show.title", read_only=True)
    type = serializers.CharField(source="show.type", read_only=True)
    
    class Meta:
        model = Watchlists
        fields = ['show_id', 'status', 'owner', 'show', 'img', 'title', 'type', 'comment', 'rating', 'created_dt']