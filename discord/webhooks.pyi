import typing
from typing import Any

from .embed import Embed
from .file import File
from .snowflake import Snowflakeish

class WebhookAdapter:
    rest: Any
    def __init__(self) -> None: ...
    def fetch_webhook(self, id, token): ...
    def modify_webhook(
        self,
        id,
        token,
        name: typing.Optional[str] = ...,
        avatar: typing.Optional[str] = ...,
    ): ...
    def delete_webhook(self, id, token): ...
    def fetch_message(self, id, token, message: Snowflakeish): ...
    def edit_message(
        self,
        id,
        token,
        message: Snowflakeish,
        content: typing.Optional[str] = ...,
        allowed_mentions: typing.Optional[bool] = ...,
    ): ...
    def delete_message(self, id, token, message: Snowflakeish): ...
    def execute(
        self,
        id,
        token,
        content: typing.Optional[str] = ...,
        username: typing.Optional[str] = ...,
        avatar_url: typing.Optional[str] = ...,
        tts: typing.Optional[bool] = ...,
        allowed_mentions: typing.Optional[bool] = ...,
        embed: typing.Optional[Embed] = ...,
        embeds: typing.Optional[typing.List[Embed]] = ...,
        flags: typing.Optional[typing.Any] = ...,
        files: typing.Optional[typing.Sequence[File]] = ...,
    ): ...

class Webhook:
    id: Any
    token: Any
    adapter: Any
    def __init__(self, id, token) -> None: ...
    def execute(
        self,
        content: typing.Optional[str] = ...,
        username: typing.Optional[str] = ...,
        avatar_url: typing.Optional[str] = ...,
        tts: typing.Optional[bool] = ...,
        allowed_mentions: typing.Optional[bool] = ...,
        embed: typing.Optional[Embed] = ...,
        embeds: typing.Optional[typing.List[Embed]] = ...,
        flags: typing.Optional[typing.Any] = ...,
        files: typing.Optional[typing.Sequence[File]] = ...,
    ): ...
