from django.db import models


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    calorie_content = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()

    has_animal_proteins = models.BooleanField()

    def __str__(self):
        return self.title


class AmountPerDay(models.Model):
    date = models.DateField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    grams = models.FloatField()

    class Meta:
        unique_together = ('date', 'ingredient')

    def __str__(self):
        return f"{self.date} - {self.ingredient.name} - {self.grams}g"
