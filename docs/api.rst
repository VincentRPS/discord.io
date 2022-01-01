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

.. attributetable:: internal.rest.RESTClient

.. autoclass:: internal.rest.RESTClient
    :members:

.. attributetable:: factories.RESTFactory

.. autoclass:: factories.RESTFactory
    :members:


WebSockets
----------

.. autoclass:: internal.websockets.DiscordClientWebSocketResponse
    :members:

AioClient
---------

.. autoclass:: RESTClientResponse
    :members:

Exceptions
----------

.. autoexception:: RPDError
    
.. autoexception:: RESTError

.. autoexception:: WebSocketError
    
.. autoexception:: Forbidden

.. autoexception:: NotFound

.. autoexception:: ServerError

Exception Hierarcy
------------------

.. exception_hierarcy::

    - :exc:`Exception`
        - :exc:`RPDError`
            - :exc:`RESTError`
                - :exc:`Forbidden`
                - :exc:`NotFound`
                - :exc:`ServerError`
            - :exc:`WebSocketError`