from django_filters.filters import RangeField
from django import forms
from django_filters.rest_framework import RangeFilter


class DateRangeFieldNew(RangeField):
    """
    Поле как и DateFromToRangeFilter в django_filters только
    не переводить в datetime.datetime и стандартное решение работает
    с временем которое нам не нужно т.к аренда идет на сутки
    """
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateField(),
            forms.DateField())
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            start_date, stop_date = data_list
            return [start_date, stop_date]
        return None


class CustomDateFromToRangeFilter(RangeFilter):
    """
    Кастомный фильтр для установеи нормальнього суфикса и простоты фильтрации
    """
    field_class = DateRangeFieldNew