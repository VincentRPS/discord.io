from typing import Any, List, Optional

from discord.types import allowed_mentions

from ..embed import Embed
from ..types import Dict

class Interaction:
    data: Any
    state: Any
    def __init__(self, data: Dict, state) -> None: ...
    token: Any
    type: Any
    guild_id: Any
    channel_id: Any
    id: Any
    options: Any
    message: Any
    def collect_children(self, data) -> None: ...
    def followup(
        self,
        content: Optional[str] = ...,
        tts: bool = ...,
        embed: Optional[Embed] = ...,
        embeds: Optional[List[Embed]] = ...,
    ): ...
    invisable: Any
    def respond(
        self,
        content: Optional[str] = ...,
        tts: bool = ...,
        embed: Optional[Embed] = ...,
        embeds: Optional[List[Embed]] = ...,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = ...,
        type: Optional[int] = ...,
        invisable: Optional[bool] = ...,
    ): ...
    def defer(self, invisable: bool = ...): ...
    @property
    def member(self): ...
