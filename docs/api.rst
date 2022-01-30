.. currentmodule:: rpd

API Reference
=============
The full RPD API Reference.

Version Specific Details
------------------------
There is currently 2 ways to get version info

The easiest is via ``__version__``

.. data:: __version__

    A string representation of the version. e.g. ``'0.3.0'``. This is based
    off of :pep:`440`.

And second is by using ``version_info``

.. data:: version_info

    A named tuple that is similar to :obj:`py:sys.version_info`.

    Just like :obj:`py:sys.version_info` the valid values for ``releaselevel`` are
    'alpha', 'beta', 'candidate' and 'final'.


REST API
--------

.. attributetable:: RESTClient

.. autoclass:: RESTClient
    :members:

.. attributetable:: RESTFactory

.. autoclass:: RESTFactory
    :members:


Gateway's
---------

.. attributetable:: Gateway

.. autoclass:: Gateway
    :members:

.. attributetable:: VoiceGateway

.. autoclass:: VoiceGateway
    :members:

Opus
----

.. autoclass:: Encoder
    :members:

Apps
----

.. attributetable:: BasicWebhookApp

.. autoclass:: BasicWebhookApp
    :members:

.. attributetable:: WebhookApp

.. autoclass:: WebhookApp
    :members:

.. attributetable:: BotApp

.. autoclass:: BotApp
    :members:

Webhooks
--------

.. attributetable:: Webhook

.. autoclass:: Webhook
    :members:

Dispatcher
----------

.. attributetable:: Dispatcher

.. autoclass:: Dispatcher
    :members:

Snowflakes
----------

.. autoclass:: Snowflakeish
    
    A Discord Snowflake.

.. autoclass:: SnowflakeishList

    A list of Snowflakes

.. autoclass:: SnowflakeishOr

    A Snowflake or object class.

Exceptions
----------

.. autoexception:: RPDError
    
.. autoexception:: RESTError
    
.. autoexception:: Forbidden

.. autoexception:: NotFound

Exception Hierarcy
------------------

.. exception_hierarchy::

    - :exc:`Exception`
        - :exc:`RPDError`
            - :exc:`RESTError`
                - :exc:`Forbidden`
                - :exc:`NotFound`
                - :exc:`ServerError`
