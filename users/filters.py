import django_filters
from users.models import User


class EmployeeFilter(django_filters.FilterSet):
    dismissed_date = django_filters.DateFromToRangeFilter()
    dismissed_date_specific = django_filters.DateFilter(
        field_name="dismissed_date", lookup_expr="exact"
    )

    class Meta:
        model = User
        fields = [
            "dismissed",
            "dismissed_date",
            "dismissed_date_specific",
            "employee_position",
            "full_name",
        ]
