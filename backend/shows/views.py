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
    def info(self, request):
        query = dict(request.query_params)
        id = query['id'][0] 
        model_type = query['type'][0]
        
        tmdb = TMDB()
        result = tmdb.get_info(id, model_type)
        return Response(result, status=200)
    
    @action(methods=['get'],detail=False)
    def get_cast(self, request):
        query = dict(request.query_params)
        id = query['id'][0] 
        model_type = query['type'][0]
        
        tmdb = TMDB()
        result = tmdb.get_full_cast_info(id, model_type)
        return Response(result, status=200)
    
    @action(methods=['get'],detail=False)
    def get_tv(self, request):       
        tmdb = TMDB()
        result = tmdb.get_tv_page()
        return Response(result, status=200)
    
    @action(methods=['get'],detail=False)
    def get_movie(self, request):       
        tmdb = TMDB()
        result = tmdb.get_movie_page()
        return Response(result, status=200)
    
class AuthenticatedShowsView(viewsets.ModelViewSet):
    serializer_class = ShowsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        permission_classes = [permissions.IsAuthenticated]

        tmdb = TMDB()
        result = tmdb.insert_info(request.data['id'], request.data['type'])[0]        
        request.POST._mutable = True
        watchlist = {"status" : request.data['status'], "comment": request.data['comments'], "rating": request.data['rating']}
        del request.data['status']
        del request.data['comments']
        del request.data['rating']
        
        show_exists = Shows.objects.filter(id = request.data['id']).count()
        if show_exists == 0:
            serializer = ShowsSerializer(data=result)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                
        watchlist['show'] = request.data['id']
        
        watchlist_exists = Watchlists.objects.filter(owner=request.user).filter(show=watchlist['show'])
        if not watchlist_exists:
            watchlist_serializer = WatchlistSerializers(data=watchlist)
            if watchlist_serializer.is_valid(raise_exception=False):
                watchlist_serializer.save(owner=request.user)
                return Response(watchlist_serializer.data, status=201)
        else:
            watchlist_exists[0].status  = watchlist['status']
            watchlist_exists[0].comment = watchlist['comment']
            watchlist_exists[0].rating = watchlist['rating']
            watchlist_exists[0].save()
            
            qs = Watchlists.objects.all().filter(owner=self.request.user)
            serializer = WatchlistSerializers(qs, many=True)
            return Response(serializer.data, status=200)

        return Response({}, status=400)
