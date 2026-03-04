import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    owner = django_filters.CharFilter(field_name="owner__username", lookup_expr="icnotains")

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'title', 'owner']