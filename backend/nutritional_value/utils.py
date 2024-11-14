from django.db.models import Count, F, Sum
from django.db.models.functions import TruncMonth, TruncWeek


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

    return {**totals, 'total_count': total_count}


def get_dynamics_of_changes(cut_size, amounts):

    if cut_size == 'month':
        dynamics_of_changes = amounts.values(
            month=TruncMonth('date')
        ).annotate(
            total_calories=Sum(
                F('ingredient__calorie_content') * F('grams') / 100
            ),
            total_proteins=Sum(F('ingredient__proteins') * F('grams') / 100),
            total_fats=Sum(F('ingredient__fats') * F('grams') / 100),
            total_carbohydrates=Sum(
                F('ingredient__carbohydrates') * F('grams') / 100
            )
        ).order_by('month')
    elif cut_size == 'week':
        dynamics_of_changes = amounts.values(week=TruncWeek('date')).annotate(
            total_calories=Sum(
                F('ingredient__calorie_content') * F('grams') / 100
            ),
            total_proteins=Sum(F('ingredient__proteins') * F('grams') / 100),
            total_fats=Sum(F('ingredient__fats') * F('grams') / 100),
            total_carbohydrates=Sum(
                F('ingredient__carbohydrates') * F('grams') / 100
            )
        ).order_by('week')
    else:
        dynamics_of_changes = amounts.values('date').annotate(
            total_calories=Sum(
                F('ingredient__calorie_content') * F('grams') / 100
            ),
            total_proteins=Sum(F('ingredient__proteins') * F('grams') / 100),
            total_fats=Sum(F('ingredient__fats') * F('grams') / 100),
            total_carbohydrates=Sum(
                F('ingredient__carbohydrates') * F('grams') / 100
            )
        ).order_by('date')

    return dynamics_of_changes
