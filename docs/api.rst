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

.. autoclass:: WebhookAdapter
    :members:

.. autoclass:: Webhook
    :members:

Colors
------

.. autoclass:: Color
    :members:

.. autoclass:: Colour
    :members:

Dispatcher
----------

.. autoclass:: Dispatcher
    :members:

Types
-----

.. autoclass:: Message
    :members:

.. autoclass:: User
    :members:

.. autoclass:: Member
    :members:

Guild
-----

.. autoclass:: Guild
    :members:

.. autoclass:: Role
    :members:

.. autoclass:: ScheduledEvent
    :members:

.. autoclass:: ScheduledEventMetadata
    :members:

.. autoclass:: WelcomeScreen
    :members:

.. autoclass:: WelcomeChannel
    :members:

.. autoclass:: Ban
    :members:

Assets
------

.. autoclass:: Emoji
    :members:

.. autoclass:: PartialEmoji
    :members:

.. autoclass:: Sticker
    :members:

.. autoclass:: Attachment
    :members:

Channels
--------

.. autoclass:: Category
    :members:

.. autoclass:: TextChannel
    :members:

.. autoclass:: VoiceChannel
    :members:

.. autoclass:: DMChannel
    :members:

.. autoclass:: GroupDMChannel
    :members:

.. autoclass:: Thread
    :members:

.. autoclass:: ThreadMetadata
    :members:

.. autoclass:: ThreadMember
    :members:

.. autoclass:: StageInstance
    :members:


Event Reference
---------------

Guilds
~~~~~~

.. autoclass:: OnGuildJoin

.. autoclass:: OnGuildUpdate

.. autoclass:: OnGuildLeave

.. autoclass:: OnGuildBan

.. autoclass:: OnGuildBanRemove

.. autoclass:: OnGuildEmojisUpdate

.. autoclass:: OnGuildIntegrationsUpdate

.. autoclass:: OnGuildStickersUpdate

.. autoclass:: OnMemberJoin

.. autoclass:: OnMemberLeave

.. autoclass:: OnMemberUpdate

.. autoclass:: OnRoleCreate

.. autoclass:: OnRoleDelete

.. autoclass:: OnRoleUpdate

.. autoclass:: OnScheduledEventCreate

.. autoclass:: OnScheduledEventDelete

.. autoclass:: OnScheduledEventJoin

.. autoclass:: OnScheduledEventLeave

.. autoclass:: OnScheduledEventUpdate

Messages
~~~~~~~~

.. autoclass:: OnMessage

.. autoclass:: OnMessageEdit

.. autoclass:: OnMessageDelete

.. autoclass:: OnMessageDeleteBulk

.. autoclass:: OnMessageReactionAdd

.. autoclass:: OnMessageReactionRemove

.. autoclass:: OnMessageReactionRemoveAll
    
.. autoclass:: OnMessageReactionRemoveEmoji


Channels
~~~~~~~~

.. autoclass:: OnChannelCreate

.. autoclass:: OnChannelDelete

.. autoclass:: OnChannelPinsUpdate

.. autoclass:: OnChannelUpdate

.. autoclass:: OnThreadCreate

.. autoclass:: OnThreadDelete

.. autoclass:: OnThreadListSync

.. autoclass:: OnThreadMembersUpdate

.. autoclass:: OnThreadMemberUpdate

.. autoclass:: OnThreadUpdate

Interactions
~~~~~~~~~~~~

.. autoclass:: OnInteraction

Etc
~~~

.. autoclass:: OnInviteCreate

.. autoclass:: OnInviteDelete

.. autoclass:: OnStageInstanceCreate

.. autoclass:: OnStageInstanceDelete

.. autoclass:: OnStageInstanceEdit

.. autoclass:: OnTyping

.. autoclass:: OnUserUpdate
    
.. autoclass:: OnWebhooksUpdate


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
    :members:

Embed
-----

.. autoclass:: Embed
    :members:

Interaction
-----------

.. autoclass:: Interaction
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
