SkyBiometry Face Detection and Recognition API client library
=============================================================

SkyBiometry Face Detection and Recognition REST API client library.

For a demonstration how to use this library, see EXAMPLE.RST.

For more information about the API and the return values, visit the `official documentation`_.

Performing actions involving Facebook or Twitter users
======================================================

If you want to perform actions involving Facebook or Twitter users you need to provide the necessary credentials.

#. **Facebook**::

    client.set_facebook_oauth_credentials('FB_USER_ID', 'FB_SESSION_ID', 'FB_OAUTH_TOKEN')

#. **Twitter (OAuth)**::

    client.set_twitter_oauth_credentials('OAUTH_USER', 'OAUTH_SECRET', 'OAUTH_TOKEN')

.. _official documentation: http://www.skybiometry.com/Documentation
