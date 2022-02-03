=====
Servicevis
=====

Servicevis is a Django app to visualise a network of services. 

Quick start
-----------

1. Add "servicevis" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'servicevis',
    )

2. Include the servicevis URLconf in your project urls.py like this::

    url(r'^servicevis/', include('servicevis.urls')),

3. Run `python manage.py migrate` to create the servicevis models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create (you'll need the Admin app enabled).

