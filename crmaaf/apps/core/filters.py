import django_filters
from crmaaf.apps.core.services.widgets import *
from .models import OrderInstance
from django.db.models import Q


class OrderFilter(django_filters.FilterSet):
    
    title = django_filters.CharFilter(lookup_expr='icontains')
    id_document = django_filters.CharFilter(lookup_expr='icontains')
    due_back = django_filters.DateFilter(widget=DateInput())

    dateperiod_day_start = django_filters.NumberFilter(label='День Начало', field_name='due_back', lookup_expr='day__gte')
    dateperiod_day_end = django_filters.NumberFilter(label='День Конец', field_name='due_back', lookup_expr='day__lte')

    dateperiod_month_start = django_filters.NumberFilter(label='Месяц Начало', field_name='due_back', lookup_expr='month__gte')
    dateperiod_month_end = django_filters.NumberFilter(label='Месяц Конец', field_name='due_back', lookup_expr='month__lte')
    
    dateperiod_year_start = django_filters.NumberFilter(label='Год Начало', field_name='due_back', lookup_expr='year__gte')
    dateperiod_year_end = django_filters.NumberFilter(label='Год Конец', field_name='due_back', lookup_expr='year__lte')

    class Meta:
        model = OrderInstance
        fields = ['title', 'due_back', 'status', 'type_order', 'id_document', 
                  'dateperiod_day_start', 'dateperiod_day_end',
                  'dateperiod_month_start', 'dateperiod_month_end',
                  'dateperiod_year_start', 'dateperiod_year_end',]

    @property
    def qs(self):
        self.parent = super().qs
        self.user = getattr(self.request, 'user', None)

        if self.user.groups.filter(name__in=['Sales Department']) \
        or self.user.is_superuser:
            return self.parent

        elif self.user.groups.filter(name__in=['Controlling']).exists() \
        and not self.user.groups.filter(name__in=["BOSS"]).exists():
            return self.parent.exclude(Q(status = 'p') | Q(status = 'w')).filter( 
                                                                                  Q(controlling = self.user.id) | 
                                                                                  Q(controlling_allow = self.user.id) | 
                                                                                  Q(controlling_disallow = self.user.id)).distinct().all()

        elif self.user.groups.filter(name__in=['BOSS']).exists() \
        and not self.user.groups.filter(name__in=["Sales Department"]).exists():
            return self.parent.exclude(status = 'p').filter(
                                                      Q(controlling = self.request.user.id) | 
                                                      Q(controlling_allow = self.request.user.id) | 
                                                      Q(controlling_disallow = self.request.user.id)).distinct().all()

        else:
            return self.parent.exclude(Q(status = 'p') | Q(status = 'w' ) | Q(status = 'j')).distinct().all()
            
    pass