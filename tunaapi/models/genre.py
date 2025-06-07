from django.db import models

class Genre(models.Model):
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ['description']

class SongGenreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('genre_id', 'song_id')

    def filter_by_genre(self, genre):
        return self.filter(genre_id=genre)

    def filter(self, *args, **kwargs):
        if 'genre' in kwargs:
            kwargs['genre_id'] = kwargs.pop('genre')
        return super().filter(*args, **kwargs)

class SongGenre(models.Model):
    song_id = models.ForeignKey('Song', on_delete=models.CASCADE, related_name='song_genres')
    genre_id = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='song_genres')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='proxy_genre', db_column='genre_id')

    objects = SongGenreManager()

    class Meta:
        db_table = 'song_genre'

    @property
    def song(self):
        return self.song_id

    @song.setter
    def song(self, value):
        self.song_id = value

    @property
    def genre(self):
        return self.genre_id

    @genre.setter
    def genre(self, value):
        self.genre_id = value
