from django.db.models import Count, F, Sum


def get_total_nutrients(objects):
    total_data = objects.aggregate(
        total_calories=Sum(
            F('ingredient__calorie_content') * F('grams') / 100
        ),
        total_proteins=Sum(F('ingredient__proteins') * F('grams') / 100),
        total_fats=Sum(F('ingredient__fats') * F('grams') / 100),
        total_carbohydrates=Sum(
            F('ingredient__carbohydrates') * F('grams') / 100
        ),
        total_count=Count('id')
    )

    total_count = total_data['total_count'] or 0
    totals = {
        key: total_data[key] or 0 for key in [
            'total_calories', 'total_proteins',
            'total_fats', 'total_carbohydrates'
        ]
    }

    averages = {}
    for key, value in totals.items():
        average_key = f'average_{key.split("_")[1]}'
        averages[average_key] = value / total_count if total_count else 0

    return {**totals, **averages, 'total_count': total_count}
