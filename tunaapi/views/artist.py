from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.artist import Artist

class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    bio = serializers.CharField()

class ArtistViewSet(ViewSet):
    def list(self, request):
        # Query the database for all artists
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        # Retrieve a specific artist by ID
        artist = Artist.objects.get(pk=pk)
        songs = artist.songs.all()  # Fetch songs associated with the artist

        # Serialize artist and songs
        artist_data = {
            "id": artist.id,
            "name": artist.name,
            "age": artist.age,
            "bio": artist.bio,
            "song_count": songs.count(),
            "songs": [
                {
                    "id": song.id,
                    "title": song.title,
                    "album": song.album,
                    "length": song.length
                }
                for song in songs
            ]
        }

        return Response(artist_data, status=status.HTTP_200_OK)

    def create(self, request):
        # Create a new artist
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            artist = Artist.objects.create(
                name=serializer.validated_data['name'],
                age=serializer.validated_data['age'],
                bio=serializer.validated_data['bio']
            )
            serializer = ArtistSerializer(artist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Delete an artist by ID
            artist = Artist.objects.get(pk=pk)
            artist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        # Update an existing artist
        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()

        # Serialize the updated artist and return the response
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)
