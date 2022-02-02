.. currentmodule:: discord

API Reference
=============
The full discord.io API Reference.

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

.. autoclass:: RESTClient
    :members:

.. autoclass:: RESTFactory
    :members:


Gateway's
---------

.. autoclass:: Gateway
    :members:

.. autoclass:: VoiceGateway
    :members:

Opus
----

.. autoclass:: Encoder
    :members:

Apps
----

.. autoclass:: BasicWebhook
    :members:

.. autoclass:: WebhookApp
    :members:

.. autoclass:: BotApp
    :members:

Webhooks
--------

.. autoclass:: Webhook
    :members:

Dispatcher
----------

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

State
-----

.. autoclass:: ConnectionState

Exceptions
----------

.. autoexception:: DiscordError
    
.. autoexception:: RESTError
    
.. autoexception:: Forbidden

.. autoexception:: NotFound

.. autoexception:: ServerError

Exception Hierarcy
------------------

.. exception_hierarchy::

    - :exc:`Exception`
        - :exc:`DiscordError`
            - :exc:`RESTError`
                - :exc:`Forbidden`
                - :exc:`NotFound`
                - :exc:`ServerError`
