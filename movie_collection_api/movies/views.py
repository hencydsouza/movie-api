import os
import requests
from requests.auth import HTTPBasicAuth
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Collection, Movie
from .serializers import UserSerializer, CollectionSerializer, MovieSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .middleware import RequestCounterMiddleware
from django.contrib.auth.models import User  
from rest_framework import generics, permissions
from .serializers import UserSerializer
from rest_framework import status 

# Function to fetch movies from the external API
def fetch_movies(page=1):
    url = f"https://demo.credy.in/api/v1/maya/movies/?page={page}"
    username = os.getenv("MOVIE_API_USERNAME")
    password = os.getenv("MOVIE_API_PASSWORD")
    
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong:",err)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class MoviesListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        page = request.GET.get('page', 1)
        movies = fetch_movies(page)
        return Response(movies)

class CollectionListView(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse({"requests": RequestCounterMiddleware.get_request_count()})

class ResetRequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        RequestCounterMiddleware.request_count = 0
        return JsonResponse({"message": "Request count reset successfully"})