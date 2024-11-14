from django import forms
from django.contrib.auth import get_user_model

from .models import AmountPerDay, Ingredient


User = get_user_model()


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


class AmountPerDayForm(forms.ModelForm):
    class Meta:
        model = AmountPerDay
        fields = ['date', 'ingredient', 'grams']
        labels = {
            'date': 'Дата',
            'ingredient': 'Ингредиент',
            'grams': 'Количество грамм',
        }
        widgets = {'date': forms.DateInput(attrs={
            'type': 'date',
        })}


class FilterIngredientForm(forms.Form):
    author = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False, label='Автор'
    )


class FilterAmountPerDayForm(forms.Form):
    CUT_SIZE_OPTIONS = [
        ('day', 'по дням'),
        ('week', 'по неделям'),
        ('month', 'по месяцам'),
    ]
    cut_size = forms.ChoiceField(
        choices=CUT_SIZE_OPTIONS, label="Выберите вариант группировки",
        initial=CUT_SIZE_OPTIONS[0][0]
    )
    date_start = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'date'
        }),
        label="От"
    )
    date_stop = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'date'
        }),
        label="По (включительно)"
    )
