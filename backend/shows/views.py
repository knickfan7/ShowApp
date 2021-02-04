import collections
from django.shortcuts import render

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated


from .serializers import ShowsSerializer
from .models import Shows
from watchlists.serializers import WatchlistSerializers, Watchlists
from .api.tmdb import TMDB

class ShowsView(viewsets.ModelViewSet):
    serializer_class = ShowsSerializer
    
    def list(self, request):
        tmdb = TMDB()
        title = (self.request.query_params.get("title"))
        result = tmdb.get_search_results(title)
        return Response(result)
    
    @action(methods=['get'],detail=False)
    def info(self,request):
        query = dict(request.query_params)
        id = query['id'][0] 
        model_type = query['type'][0]
        
        tmdb = TMDB()
        result = tmdb.get_info(id, model_type)
        return Response(result, status=200)
    
class AuthenticatedShowsView(viewsets.ModelViewSet):
    serializer_class = ShowsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        permission_classes = [permissions.IsAuthenticated]

        tmdb = TMDB()
        result = tmdb.insert_info(request.data['id'], request.data['type'])[0]        
        request.POST._mutable = True
        show = {"name" : request.data['show']}
        del request.data['show']
        
        show_exists = Shows.objects.filter(id = request.data['id']).count()
        if show_exists == 0:
            serializer = ShowsSerializer(data=result)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                
        show['show'] = request.data['id']
        
        watchlist_exists = Watchlists.objects.filter(owner=request.user).filter(show=show['show'])
        if not watchlist_exists:
            watchlist_serializer = WatchlistSerializers(data=show)
            
            if watchlist_serializer.is_valid(raise_exception=True):
                watchlist_serializer.save(owner=request.user)
                return Response(watchlist_serializer.data, status=201)
            
        return Response({}, status=400)
