# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
"""
The ConnectionState Caches most things during connection.
"""
import asyncio
from collections import OrderedDict
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Tuple,
    TypeVar,
    Union,
    overload
)

if TYPE_CHECKING:
    from .client import Client
    from .ext.commands import Command

__all__: List = ['Hold', 'ConnectionState']

T = TypeVar('T')
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]


# so there are 2 pretty big problems with this right now,
# 1 it's not async so the db would have to be blocking
# 2 it's repetitive to switch out since you need to switch all cache objects.
class Hold:
    """A hold of cache, easily swapable with a db."""

    def __init__(self):
        self._cache = OrderedDict()

    def view(self) -> List[Dict]:
        self._cache.values()

    def list(self):
        return self._cache.items()

    def new(self, name: str, data: Union[str, int, Dict, Any]):
        self._cache[name] = data

    def edit(self, name: str, data: Union[str, int, Dict, Any]):
        self._cache.update({name: data})

    @overload
    def get(self, name: str):
        return self._cache.get(name)

    @overload
    def get(self, name: str, __default: Any):
        return self._cache.get(name, __default)

    @overload
    def pop(self, name: str):
        return self._cache.pop(name)

    @overload
    def pop(self, name: str, __default: Any):
        return self._cache.pop(name, __default)

    def reset(self) -> None:
        self._cache.clear()
    
    def cache_for(self, name: str, data: Any, time: float):
        self._cache[name] = data
        asyncio.create_task(self.delete_after(name=name, time=time))

    async def delete_after(self, *, name: str, time: float):
        await asyncio.sleep(time)
        del self._cache[name]

class Stream:
    def __init__(self, __name: str, __data: dict):
        self.__name__ = __name
        self._formulate_data(__data)
    
    def _formulate_data(self, _d: dict):
        self.data = {
            'stream': self.__name__,
            'data': _d
        }
    
    def __repr__(self) -> Dict:
        return self.data

class HTTPStream(Stream):
    def __init__(self, __data: dict):
        self.__name__ = 'http'
        self._formulate_data(__data)

    def _formulate_data(self, _d: dict):
        self.data = {
            'stream': 'http',
            'data': {
                'Route': _d.get('route'),
                'X-RateLimit': {
                    'Limit': _d.get('limit'),
                    'Global': _d.get('global', False),
                    'Bucket': _d.get('ratelimit_bucket'),
                },
                'Max-Retries': 5,
                'Data': _d.get('data'),
                'Bucket': _d.get('bucket')
            }
        }

class ShardStream(Stream):
    def __init__(self, __data: dict):
        self.__name__ = 'shard'
        self._formulate_data(__data)
    
    def _formulate_data(self, _d: dict):
        self.data = {
            'stream': self.__name__,
            'data': {
                'intents': _d.get('intents', 0),
                'active': _d.get('active', []),
                'pending': _d.get('pending', 0),
                'session_ids': _d.get('session_ids', []),
                'ready': _d.get('ready', [])
            }
        }
    
    def edit(self, _d: dict):
        self.data = {
            'stream': self.__name__,
            'data': {
                'intents': _d.get('intents', 0),
                'active': _d.get('active', []),
                'pending': _d.get('pending', []),
                'session_ids': _d.get('session_ids', []),
                'ready': _d.get('ready', [])
            }
        }

class ConnectionState:
    """The Connection State

    .. versionadded:: 0.4.0

    .. note::

        The connection state is responsible for caching
        everything, meaning most classes will depend on it.

    Attributes
    ----------
    _bot_intents: :class:`int`
        The cached bot intents, used for Gateway

    _session_id: :class:`int`
        The Gateway, session id

    _voice_session_id: :class:`int`
        The Voice Gateway Session ID

    _seq: :class:`int`
        The Gateway seq number, can be None.

    app: :class:`Client`
        The bot app

        .. versionadded:: 0.5.0

    _said_hello: :class:`bool`
        If the Gateway got a hello or not.

    loop :class:`asyncio.AbstractEventLoop`
        The current loop

    _bot_presences: :class:`list`
        A list of the bots presences

    _bot_status: :class:`str`
        The bot status, e.g. online

    _bot_presence_type: :class:`int`
        The bot presence type, defaults to 0

    listeners: :class:`dict`
        The bot listeners

    shard_count: :class:`int`
        the number of shards.

        .. versionadded:: 0.6.0
    """

    def __init__(self, *, timeout: int = 1000, **options):

        # core cache holds
        self.guilds = options.get('guild_cache_hold') or Hold()
        self.members = options.get('members_cache_hold') or Hold()
        self.roles = options.get('roles_cache_hold') or Hold()
        self.guild_events = options.get('guild_events_cache_hold') or Hold()
        self.channels = options.get('channel_cache_hold') or Hold()
        self.messages = options.get('messages_cache_hold') or Hold()
        self.stage_instances = options.get('stage_instances_cache_hold') or Hold()

        self._ready: asyncio.Event = asyncio.Event()

        self.streams: List[Stream] = []
        self.http_streams: List[HTTPStream] = []
        self.shard_streams: List[ShardStream] = []

        self._bot_intents: int = options.get('intents')
        """The cached bot intents, used for Gateway"""

        self._bot_id: int = None

        self.bot_info = {}

        self._voice_session_id: int = None

        self._seq: int = None
        """The seq number"""

        self.app: Client = options.get('bot', None)
        """The bot app"""

        self._said_hello: bool = False
        """If the Gateway got a hello or not."""

        self.loop: asyncio.AbstractEventLoop = options.get('loop', None)
        """The current loop"""

        self._bot_presences: List[str, Any] = []
        """The precenses"""

        self._bot_status: str = 'online'
        """The status"""

        self._bot_presence_type: int = 0
        """Precense type"""

        self.listeners: Dict[str, List[Tuple[asyncio.Future, Callable[..., bool]]]] = {}
        """The listeners"""

        self.shard_count: int = options.get('shard_count', None)
        """The shard count"""

        self.components: Dict[str, Any] = {}

        self.prefixed_commands: List[Command] = []

        self.application_commands: Dict[str, Any] = {}

        self.prefix = options.get('prefix')

        self.timeout = timeout

        self.loop.create_task(self.clear_cache())

    async def clear_cache(self):
        await asyncio.sleep(self.timeout)
        self.messages.reset()
        self.http_streams.clear()
        self.streams.clear()
        self.stage_instances.reset()
        self.loop.create_task(self.clear_cache())


def member_cacher(state: ConnectionState, data: Any):
    for member in data:
        state.members.new(member['id'], member)
