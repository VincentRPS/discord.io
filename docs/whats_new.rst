Changelog
=========
The discord.io version changelog

.. note::

    This only covers changes after release 0.8.0

.. _vp0p9p0:

2.0.0
-----
This is the discord.io rewrite and is built upon reworking and speeding up the previous versions.

.. todo:: Work on this part.

.. _vp0p8p0:

0.8.0
-----

Features
~~~~~~~~

- Events had a overhaul, most of the api events are now supported
- There are many more model types now, just to count some;

    - ScheduledEvent
    - Thread
    - TextChannel
    - ScheduledEventMetadata
    - ThreadMetadata

    and many more!

Fixes
~~~~~

- Fixed error with zlib compression errors and aiohttp errors with multiple shards, :issue:`38`