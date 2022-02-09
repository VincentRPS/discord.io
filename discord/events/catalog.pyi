from discord.types import Dict as Dict

from ..guild import ScheduledEvent as ScheduledEvent
from ..member import Member as Member
from ..state import ConnectionState as ConnectionState
from ..state import member_cacher as member_cacher
from .guilds import OnGuildBan as OnGuildBan
from .guilds import OnGuildBanRemove as OnGuildBanRemove
from .guilds import OnGuildEmojisUpdate as OnGuildEmojisUpdate
from .guilds import OnGuildIntegrationsUpdate as OnGuildIntegrationsUpdate
from .guilds import OnGuildJoin as OnGuildJoin
from .guilds import OnGuildLeave as OnGuildLeave
from .guilds import OnGuildStickersUpdate as OnGuildStickersUpdate
from .guilds import OnGuildUpdate as OnGuildUpdate
from .guilds import OnMemberJoin as OnMemberJoin
from .guilds import OnMemberLeave as OnMemberLeave
from .guilds import OnMemberUpdate as OnMemberUpdate
from .guilds import OnRoleCreate as OnRoleCreate
from .guilds import OnRoleDelete as OnRoleDelete
from .guilds import OnRoleUpdate as OnRoleUpdate
from .guilds import OnScheduledEventCreate as OnScheduledEventCreate
from .guilds import OnScheduledEventDelete as OnScheduledEventDelete
from .guilds import OnScheduledEventJoin as OnScheduledEventJoin
from .guilds import OnScheduledEventLeave as OnScheduledEventLeave
from .guilds import OnScheduledEventUpdate as OnScheduledEventUpdate
from .interactions import OnInteraction as OnInteraction
from .messages import OnMessage as OnMessage
from .messages import OnMessageDelete as OnMessageDelete
from .messages import OnMessageEdit as OnMessageEdit

class Cataloger:
    def __init__(self, data: Dict, dis, state: ConnectionState) -> None: ...
