from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.song import Song
from tunaapi.models.artist import Artist

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
        song = Song.objects.get(pk=pk)
        serializer = self.SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
