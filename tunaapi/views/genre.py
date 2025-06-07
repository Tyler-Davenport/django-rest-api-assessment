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
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
