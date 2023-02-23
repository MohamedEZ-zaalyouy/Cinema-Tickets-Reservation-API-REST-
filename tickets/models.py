from django.db import models

# Create your models here.

class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self) -> str:
        return self.movie


class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='Reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='Reservation', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.guest