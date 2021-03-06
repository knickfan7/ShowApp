from django.shortcuts import render

from rest_framework import permissions, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from .models import Watchlists
from .serializers import WatchlistSerializers

class WatchlistView(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializers
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        qs = Watchlists.objects.all().filter(owner=self.request.user)
        serializer = WatchlistSerializers(qs, many=True)
        return Response(serializer.data, status=200)

    
    @action(methods=['get'],detail=False)
    def get_show(self, request):
        query = dict(request.query_params)
        id = query['id'][0] 
        qs = Watchlists.objects.all().filter(show=id).filter(owner=self.request.user)
        
        if len(qs) > 0:
            serializer = WatchlistSerializers(qs, many=True)
            return Response(serializer.data, status=200)
        return Response({}, status=404)
    
    def create(self, request): 
        serializer = WatchlistSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response({}, status=401)
