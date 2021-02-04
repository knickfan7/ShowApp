from rest_framework import serializers

from .models import Shows

class ShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shows
        fields = ['id', 'title', 'image', 'type']
        
    def __str__(self):
        return self.title
        