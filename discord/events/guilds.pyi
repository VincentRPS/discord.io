from ..assets import Emoji as Emoji
from ..assets import Sticker as Sticker
from ..guild import Guild as Guild
from ..guild import Role as Role
from ..guild import ScheduledEvent as ScheduledEvent
from ..member import Member as Member
from ..user import User as User
from .core import Event as Event

class OnGuildJoin(Event):
    def process(self) -> None: ...

class OnGuildUpdate(Event):
    def process(self) -> None: ...

class OnGuildLeave(Event):
    def process(self) -> None: ...

class OnGuildBan(Event):
    def process(self) -> None: ...

class OnGuildBanRemove(Event):
    def process(self) -> None: ...

class OnGuildIntegrationsUpdate(Event):
    def process(self) -> None: ...

class OnGuildEmojisUpdate(Event):
    def process(self) -> None: ...

class OnGuildStickersUpdate(Event):
    def process(self) -> None: ...

class OnMemberJoin(Event):
    def process(self) -> None: ...

class OnMemberLeave(Event):
    def process(self) -> None: ...

class OnMemberUpdate(Event):
    def process(self) -> None: ...

class OnRoleCreate(Event):
    def process(self) -> None: ...

class OnRoleUpdate(Event):
    def process(self) -> None: ...

class OnRoleDelete(Event):
    def process(self) -> None: ...

class OnScheduledEventCreate(Event):
    def process(self) -> None: ...

class OnScheduledEventUpdate(Event):
    def process(self) -> None: ...

class OnScheduledEventDelete(Event):
    def process(self) -> None: ...

class OnScheduledEventJoin(Event):
    def process(self) -> None: ...

class OnScheduledEventLeave(Event):
    def process(self) -> None: ...
