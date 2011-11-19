face.com Python API client library
==================================

face.com_ REST API Python client library.

For a demonstration how to use this library, see EXAMPLE.RST.

For more information about the API and the return values, visit the `official documentation`_.

Performing actions involving Facebook or Twitter users

Dependencies:
poster - pip install poster [ http://pypi.python.org/pypi/poster/0.4 ]
======================================================

If you want to perform actions involving Facebook or Twitter users you need to provide the necessary credentials.

#. **Facebook**::

    client.facebookCredentials('FB_USER_ID','FB_OAUTH_TOKEN')

#. **Twitter (OAuth)**::

    client.twitterCredentials('OAUTH_USER', 'OAUTH_SECRET', 'OAUTH_TOKEN')

.. _face.com: http://developers.face.com/
.. _official documentation: http://developers.face.com/docs/api/
