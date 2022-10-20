the_activity
===============

This app can be installed and used in your django project by:

.. code-block:: bash

    $ pipenv install git+https://github.com/zerobit-tech/the_activity@main#egg=the_activity


Edit your `settings.py` file to include `'the_activity'` in the `INSTALLED_APPS`
listing.

.. code-block:: python

    INSTALLED_APPS = [
        ...

        'the_activity',
    ]

    # ------------------------------------------------------
    # django-otp
    # ------------------------------------------------------
    OTP_TOTP_ISSUER = 'Sample THE CLIENTs APP'
    OTP_ENTRY_URL = '/twofactor/'



    MIDDLEWARE = [
        ...
   
    ]

     

 

Edit your project `urls.py` file to import the URLs:


.. code-block:: python

    url_patterns = [
        ...

        path('', include('the_activity.urls')),
    ]


Finally, add the models to your database:


.. code-block:: bash

    $ ./manage.py makemigrations the_activity


The "project" Branch
--------------------

The `master branch <https://github.com/realpython/django-receipts/tree/master>`_ contains the final code for the PyPI package. There is also a `project branch <https://github.com/realpython/django-receipts/tree/project>`_ which shows the "before" case -- the Django project before the app has been removed.


 