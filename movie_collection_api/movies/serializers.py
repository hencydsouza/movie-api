from rest_framework import serializers
from .models import Collection, Movie
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']  # Simple fields



class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies', 'uuid']
        read_only_fields = ['uuid']

    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(user=self.context['request'].user, **validated_data)
        for movie_data in movies_data:
            Movie.objects.create(collection=collection, **movie_data)
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if movies_data is not None:
            # Clear existing movies and add new ones
            instance.movies.all().delete()
            for movie_data in movies_data:
                Movie.objects.create(collection=instance, **movie_data)
        return instance
