from rest_framework import filters
from functools import reduce
from operator import or_
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Count


class Example(filters.BaseFilterBackend):
    """
    Example
    """

    def filter_queryset(self, request, queryset, view):
        """
        Example
        """
        return queryset
