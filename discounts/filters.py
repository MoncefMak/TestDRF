import django_filters

from discounts.models import HistoryDiscountCode


class HistoryDiscountCodeFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = HistoryDiscountCode
        fields = ['discount_code__code', 'created_at']
