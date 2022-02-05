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

.. autoclass:: Shard
    :members:

.. autoclass:: Gateway
    :members:

.. autoclass:: VoiceGateway
    :members:

Opus
----

.. autoclass:: Encoder
    :members:

Voice
-----

.. autoclass:: VoiceClient
    :members:

Client
------

.. autoclass:: Client
    :members:

Webhook
-------

.. autoclass:: Webhook
    :members:

Colors
------

.. autoclass:: Color
    :members:

.. autoclass:: Colour
    :members:

Webhooks
--------

.. autoclass:: Webhook
    :members:

Dispatcher
----------

.. autoclass:: Dispatcher
    :members:

Data Objects
-------------

.. autoclass:: Message
    :members:

.. autoclass:: User
    :members:

.. autoclass:: Guild
    :members:

.. autoclass:: Member
    :members:

Event Reference
---------------

.. autoclass:: OnMessage

.. autoclass:: OnMessageEdit

.. autoclass:: OnMessageDelete

.. autoclass:: OnInteraction

Snowflakes
----------

.. autoclass:: Snowflakeish
    
    A Discord Snowflake.

.. autoclass:: SnowflakeishList

    A list of Snowflakes

.. autoclass:: SnowflakeishOr

    A Snowflake or cache class.

State
-----

.. autoclass:: Hold
    :members:

.. autoclass:: ConnectionState

File
----

.. autoclass:: File
    :members:

Intents
-------

.. autoclass:: Intents

Embed
-----

.. autoclass:: Embed
    :members:

Interaction
-----------

.. autoclass:: Interaction
    :members:

Context
-------

.. autoclass:: Context
    :members:


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
