face.com Python API client library
==================================

face.com_ REST API Python client library.

For a demonstration how to use this library, see EXAMPLE.RST.

For more information about the API and the return values, visit the `official documentation`_.

Performing actions involving Facebook or Twitter users
======================================================

If you want to perform actions involving Facebook or Twitter users you need to provide the necessary credentials.

#. **Facebook**::

    client.set_facebook_credentials('FB_USER_ID', 'FACEBOOK_SESSION')

#. **Twitter (OAuth)**::

    client.set_twitter_oauth_credentials('OAUTH_USER', 'OAUTH_SECRET', 'OAUTH_TOKEN')

#. **Twitter (username and password)**::

    client.set_twitter_user_credentials('TWITTER_USERNAME', 'TWITTER_PASSWORD')

.. _face.com: http://developers.face.com/
.. _official documentation: http://developers.face.com/docs/api/
