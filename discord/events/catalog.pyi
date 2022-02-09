from ..guild import ScheduledEvent as ScheduledEvent
from ..member import Member as Member
from ..state import ConnectionState as ConnectionState, member_cacher as member_cacher
from .guilds import OnGuildBan as OnGuildBan, OnGuildBanRemove as OnGuildBanRemove, OnGuildEmojisUpdate as OnGuildEmojisUpdate, OnGuildIntegrationsUpdate as OnGuildIntegrationsUpdate, OnGuildJoin as OnGuildJoin, OnGuildLeave as OnGuildLeave, OnGuildStickersUpdate as OnGuildStickersUpdate, OnGuildUpdate as OnGuildUpdate, OnMemberJoin as OnMemberJoin, OnMemberLeave as OnMemberLeave, OnMemberUpdate as OnMemberUpdate, OnRoleCreate as OnRoleCreate, OnRoleDelete as OnRoleDelete, OnRoleUpdate as OnRoleUpdate, OnScheduledEventCreate as OnScheduledEventCreate, OnScheduledEventDelete as OnScheduledEventDelete, OnScheduledEventJoin as OnScheduledEventJoin, OnScheduledEventLeave as OnScheduledEventLeave, OnScheduledEventUpdate as OnScheduledEventUpdate
from .interactions import OnInteraction as OnInteraction
from .messages import OnMessage as OnMessage, OnMessageDelete as OnMessageDelete, OnMessageEdit as OnMessageEdit
from discord.types import Dict as Dict

class Cataloger:
    def __init__(self, data: Dict, dis, state: ConnectionState) -> None: ...
