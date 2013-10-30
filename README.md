
Django OnSite
=============

Django OnSite provides helpers for working with [Django sites framework][sites].


Installation
------------

Install the package using something like pip and add ``onsite`` to
your ``INSTALLED_APPS`` setting.


OnSite Queryset
---------------

Django provides a model manager that automatically filters only objects
associated with the current Site.

The standard Django implementation allows you to do this:

    Photo.on_site.all()

    # Equivalent to:
    Photo.objects.filter(site=settings.SITE_ID)

This implementation makes it difficult to to combine the on site filtering
with other querysets. For instance, you might want to do something like this:

    Photos.objects.published().on_site()

One way to achieve that sort of queryset chaining is to combine the QuerySet
classes that take care of filtering.

Django OnSite provides a queryset class that replicates the filtering functionality
of [Django CurrentSiteManager][current-site].

In this example we use [django-model-utils pass through manager][pass-through]
to combine several querset classes.


    # managers.py

    from datetime import datetime
    from django.db.models.query import QuerySet

    from onsite.managers import OnSiteQuerySet


    class PhotoQuerySet(QuerySet):

        def published(self):
            return self.filter(publication_date__lte=datetime.now())

        def unpublished(self):
            return self.filter(publication_date__gte=datetime.now())


    class PhotoOnSiteQuerySet(PhotoQuerySet, OnSiteQuerySet):
        pass


    # models.py

    from django.db import models

    from model_utils.managers import PassThroughManager
    from photos.managers import PhotoOnSiteQuerySet


    class Photo(models.Model):
        site = models.ForeignKey('sites.Site')
        name = models.CharField(max_length=255)
        image = models.ImageField(upload_to='photos', max_length=255)
        publication_date = models.DateTimeField()

        objects = PassThroughManager.for_queryset_class(PhotoOnSiteQuerySet)()

        def __unicode__(self):
            return self.name

        class Meta:
            verbose_name = 'photo'
            verbose_name_plural = 'phtos'


    # usage

    from photos.models import *

    Photo.objects.on_site().unpublished()

    Photo.objects.on_site().published()


OnSite Queryset and Multilingual
--------------------------------

In this next example we combine the functionality that [django-linguo][linguo]
provides through it's queryset and the queryset from django-onsite.
We use [django-model-utils][model-utils].


    # managers.py

    from linguo.managers import MultilingualQuerySet
    from onsite.managers import OnSiteQuerySet

    class MultilingualOnSiteQuerySet(MultilingualQuerySet, OnSiteQuerySet):
        pass


    # models.py

    class Product(MultilingualModel):
        sites = models.ManyToManyField('sites.Site', verbose_name='sites',
            related_name='+')
        name = models.CharField(_('name'), max_length=255)
        description = models.TextField(_('description'))

        objects = PassThroughManager.for_queryset_class(MultilingualOnSiteQuerySet)()

        class Meta:
            translate = ('name', 'description')
            verbose_name = 'product'
            verbose_name_plural = 'products'

        def __unicode__(self):
            return self.name

    # usage

        from products.models import Photos

        Product.objects.on_site()


[sites]: https://docs.djangoproject.com/en/dev/ref/contrib/sites/
[current-site]: https://docs.djangoproject.com/en/dev/ref/contrib/sites/#the-currentsitemanager
[pass-through]: https://django-model-utils.readthedocs.org/en/latest/managers.html#passthroughmanager
[model-utils]: https://django-model-utils.readthedocs.org
[linguo]: https://github.com/zmathew/django-linguo/
