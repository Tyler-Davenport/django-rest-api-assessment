from django.db import models

class Genre(models.Model):
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ['description']

class SongGenre(models.Model):
    song_id = models.ForeignKey('Song', on_delete=models.CASCADE)
    genre_id = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        db_table = 'song_genre'
