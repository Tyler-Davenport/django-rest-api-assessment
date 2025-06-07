from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.song import Song
from tunaapi.models.artist import Artist
from tunaapi.models.genre import SongGenre

class SongViewSet(ViewSet):
    class SongSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        title = serializers.CharField(max_length=100)
        artist_id = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
        album = serializers.CharField(max_length=100, allow_blank=True, required=False)
        length = serializers.IntegerField()

    def list(self, request):
        songs = Song.objects.all()
        serializer = self.SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        # Retrieve the song by ID
        song = Song.objects.get(pk=pk)

        # Fetch the artist details
        artist = song.artist_id
        artist_data = {
            "id": artist.id,
            "name": artist.name,
            "age": artist.age,
            "bio": artist.bio
        }

        # Fetch associated genres using the SongGenre table
        song_genres = song.song_genres.all()
        genres = [
            {
                "id": sg.genre_id.id,
                "description": sg.genre_id.description
            }
            for sg in song_genres
        ]

        # Construct the response data
        song_data = {
            "id": song.id,
            "title": song.title,
            "artist": artist_data,
            "album": song.album,
            "length": song.length,
            "genres": genres
        }

        return Response(song_data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.SongSerializer(data=request.data)
        if serializer.is_valid():
            song = Song.objects.create(
                title=serializer.validated_data['title'],
                artist_id=serializer.validated_data['artist_id'],  # Use artist_id directly
                album=serializer.validated_data.get('album', ''),
                length=serializer.validated_data['length']
            )
            serializer = self.SongSerializer(song)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        song = Song.objects.get(pk=pk)
        serializer = self.SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            song.title = serializer.validated_data.get('title', song.title)
            song.artist_id = serializer.validated_data.get('artist_id', song.artist_id)
            song.album = serializer.validated_data.get('album', song.album)
            song.length = serializer.validated_data.get('length', song.length)
            song.save()
            return Response(self.SongSerializer(song).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SongGenreViewSet(ViewSet):
    def list(self, request):
        # Query the database for all song-genre relationships
        song_genres = SongGenre.objects.all()
        data = [
            {
                "id": sg.id,
                "song_id": sg.song_id.id,
                "genre_id": sg.genre_id.id
            }
            for sg in song_genres
        ]
        return Response(data, status=status.HTTP_200_OK)
