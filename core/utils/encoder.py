from django.core.serializers.json import DjangoJSONEncoder
from django_countries.fields import Country

class CountriesEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Country):
            return str(obj)
        return super().default(obj)