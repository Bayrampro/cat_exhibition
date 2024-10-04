from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class Kind(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Cat(models.Model):
    color = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.ForeignKey(Kind, on_delete=models.CASCADE)

    def average_rating(self):
        average = self.ratings.aggregate(Avg('score')).get('score__avg', 0)
        return round(average, 2) if average is not None else 0

    def __str__(self):
        return f"{self.kind} - {self.color}"


class Rating(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ['user', 'cat']

    def __str__(self):
        return f"{self.cat} - {self.score}"

