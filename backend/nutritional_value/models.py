from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    calorie_content = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()

    has_animal_proteins = models.BooleanField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class AmountPerDay(models.Model):
    date = models.DateField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    grams = models.FloatField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('date', 'ingredient')

    def __str__(self):
        return f"{self.date} - {self.ingredient.title} - {self.grams}g"
