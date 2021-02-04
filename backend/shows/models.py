from django.db import models

# Create your models here.

class Shows(models.Model):
    class Meta:
        verbose_name_plural = "Shows"
            
    id = models.IntegerField(primary_key=True) # ID from TMDBMovie
    title = models.TextField()
    image = models.TextField()
    type = models.CharField(max_length=10)
    
    def __str__(self):
        return self.title
    
