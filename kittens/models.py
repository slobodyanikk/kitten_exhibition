from django.db import models
from django.contrib.auth.models import User  # Модель пользователя


# Модель для пород
class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Модель для котят
class Kitten(models.Model):
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.breed.name} ({self.color})'


class Rating(models.Model):
    kitten = models.ForeignKey('Kitten', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ('kitten', 'user')  # Каждый пользователь может оценивать одного котенка только один раз

    def __str__(self):
        return f"{self.user.username} - {self.kitten.name}: {self.rating}"
