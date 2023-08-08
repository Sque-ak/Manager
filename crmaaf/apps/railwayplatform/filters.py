from crmaaf.apps.core.services.widgets import DateInput
import django_filters
from .models import RailwayOrder


class RailwayOrderFilter(django_filters.FilterSet):

    address__name = django_filters.CharFilter(lookup_expr='icontains')
    date_of_created = django_filters.DateFilter(
        widget=DateInput(
            attrs={
                'class': 'datepicker'
            }
        ))

    class Meta:
        model = RailwayOrder
        fields = ['id', 'date_of_created', 'address', 'created_by', "type_railwayorder"]
        widgets = {'date_of_created': DateInput(),}

    pass