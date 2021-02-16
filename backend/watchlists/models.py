from django.db import models
from django.db.models.deletion import PROTECT
from django.utils import timezone

from django.contrib.auth.models import User  
from shows.models import Shows


class Watchlists(models.Model):
    class Meta:
        verbose_name_plural = "Watchlists"
    status = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name='watchlists', on_delete=models.CASCADE, null=True
    )
    show = models.ForeignKey(Shows, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    created_dt = models.DateField(editable=False)
    
    def __str__(self):
        return self.status
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_dt = timezone.now().date()
        return super(Watchlists, self).save(*args, **kwargs)
    