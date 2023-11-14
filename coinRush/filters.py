import django_filters
from .models import Stock
class StockFilters(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

