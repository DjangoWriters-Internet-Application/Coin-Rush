import django_filters
from .models import Stock
class StockFilters(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields= {"symbol":["icontains"],

            "company_name":["icontains"],
        "current_price":["lt","gt"]
        }
