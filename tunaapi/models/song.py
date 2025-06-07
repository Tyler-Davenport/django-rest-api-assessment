from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='songs')
    album = models.CharField(max_length=100, blank=True, null=True)
    length = models.IntegerField()
    genre = None  # Remove the direct ForeignKey relationship

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Song"
        verbose_name_plural = "Songs"
        ordering = ['title']

    @property
    def artist(self):
        return self.artist_id

    @artist.setter
    def artist(self, value):
        self.artist_id = value

        
