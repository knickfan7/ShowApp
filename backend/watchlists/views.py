from django.shortcuts import render

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .models import Watchlists
from .serializers import WatchlistSerializers

class WatchlistView(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializers
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        qs = Watchlists.objects.all().filter(name=self.request.query_params.get("name")).filter(owner=self.request.user)
        
        if len(qs) > 0:
            serializer = WatchlistSerializers(qs, many=True)
            return Response(serializer.data, status=200)
        return Response({}, status=404)
    
    def create(self, request): 
        serializer = WatchlistSerializers(data=request.data)
        if serializer.is_valid():
            '''On save, update user'''
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response({}, status=401)
