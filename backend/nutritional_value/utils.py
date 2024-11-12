from django.db.models import Sum, F


def get_total_nutrients(objects):
    total_count = objects.count()

    if total_count == 0:
        return {
            'total_calories_value': 0,
            'total_proteins_value': 0,
            'total_fats_value': 0,
            'total_carbohydrates_value': 0,
            'average_calories_value': 0,
            'average_proteins_value': 0,
            'average_fats_value': 0,
            'average_carbohydrates_value': 0,
            'total_count': 0
        }

    total_calories = objects.annotate(
        calories=F('ingredient__calorie_content') * F('grams')
    ).aggregate(total_calories=Sum('calories'))

    total_calories_value = total_calories['total_calories'] or 0
    average_calories_value = total_calories_value / total_count

    total_proteins = objects.annotate(
        proteins=F('ingredient__proteins') * F('grams')
    ).aggregate(total_proteins=Sum('proteins'))

    total_proteins_value = total_proteins['total_proteins'] or 0
    average_proteins_value = total_proteins_value / total_count

    total_fats = objects.annotate(
        fats=F('ingredient__fats') * F('grams')
    ).aggregate(total_fats=Sum('fats'))

    total_fats_value = total_fats['total_fats'] or 0
    average_fats_value = total_fats_value / total_count

    total_carbohydrates = objects.annotate(
        carbohydrates=F('ingredient__carbohydrates') * F('grams')
    ).aggregate(total_carbohydrates=Sum('carbohydrates'))

    total_carbohydrates_value = total_carbohydrates['total_carbohydrates'] or 0
    average_carbohydrates_value = total_carbohydrates_value / total_count

    return {
        'total_calories_value': total_calories_value,
        'total_proteins_value': total_proteins_value,
        'total_fats_value': total_fats_value,
        'total_carbohydrates_value': total_carbohydrates_value,
        'average_calories_value': average_calories_value,
        'average_proteins_value': average_proteins_value,
        'average_fats_value': average_fats_value,
        'average_carbohydrates_value': average_carbohydrates_value,
        'total_count': total_count
    }
