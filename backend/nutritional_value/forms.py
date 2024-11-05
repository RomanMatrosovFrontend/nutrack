from django import forms
from .models import Ingredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            'title', 'slug', 'description', 'calorie_content', 'proteins',
            'fats', 'carbohydrates', 'has_animal_proteins'
        ]
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'calorie_content': forms.NumberInput(attrs={'step': 0.1}),
            'proteins': forms.NumberInput(attrs={'step': 0.1}),
            'fats': forms.NumberInput(attrs={'step': 0.1}),
            'carbohydrates': forms.NumberInput(attrs={'step': 0.1}),
            'has_animal_proteins': forms.CheckboxInput(),
        }
        labels = {
            'title': 'Название ингредиента',
            'description': 'Описание',
            'calorie_content': 'Калорийность (на 100 г)',
            'proteins': 'Белки (на 100 г)',
            'fats': 'Жиры (на 100 г)',
            'carbohydrates': 'Углеводы (на 100 г)',
            'has_animal_proteins': 'Продукт животного происхожения',
        }

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if not slug.isalnum():
            raise forms.ValidationError("Slug must be alphanumeric.")
        return slug
