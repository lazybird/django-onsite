from django.conf import settings
from django.db.models.query import QuerySet


class OnSiteQuerySet(QuerySet):

    def __init__(self, *args, **kwargs):
        super(OnSiteQuerySet, self).__init__(*args, **kwargs)

        self.__field_name = None
        field_names = self.model._meta.get_all_field_names()
        for potential_name in ['site', 'sites']:
            if potential_name in field_names:
                self.__field_name = potential_name
                break

    def on_site(self):
        if self.__field_name:
            lookup_parameters = {
                self.__field_name + '__id__exact': settings.SITE_ID,
            }
            return self.filter(**lookup_parameters)
        else:
            return self.filter()
