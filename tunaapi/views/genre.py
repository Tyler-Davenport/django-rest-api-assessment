from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.genre import Genre

class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField()

class GenreViewSet(ViewSet):
    def list(self, request):
        # Query the database for all genres
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        # Retrieve a specific genre by ID
        genre = Genre.objects.get(pk=pk)

        # Fetch songs associated with the genre using the SongGenre table
        song_genres = genre.song_genres.all()
        songs = [
            {
                "id": sg.song_id.id,
                "title": sg.song_id.title,
                "artist_id": sg.song_id.artist_id.id,
                "album": sg.song_id.album,
                "length": sg.song_id.length
            }
            for sg in song_genres
        ]

        genre_data = {
            "id": genre.id,
            "description": genre.description,
            "songs": songs
        }

        return Response(genre_data, status=status.HTTP_200_OK)

    def create(self, request):
        # Create a new genre
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            genre = Genre.objects.create(
                description=serializer.validated_data['description']
            )
            serializer = GenreSerializer(genre)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Delete a genre by ID
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        # Update an existing genre
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()

        # Serialize the updated genre and return the response
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)
