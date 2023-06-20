from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from .models import Post, Category
from django.forms import DateTimeInput


class NewsFilter(FilterSet):

    post_category = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='None'
    )

    date_creation = DateTimeFilter(
        field_name='date_creation',
        lookup_expr='gt',
        label='Дата',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )

    )

    class Meta:
        model = Post
        fields = {'title': ['icontains']}




