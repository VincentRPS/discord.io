from ..channels import VoiceChannel as VoiceChannel
from ..state import ConnectionState as ConnectionState
from .gateway import VoiceGateway as VoiceGateway
from .opus import Encoder as Encoder
from .players import AudioPlayer as AudioPlayer
from discord import utils as utils
from typing import Any, List, Tuple

has_nacl: bool

class VoiceClient:
    endpoint_ip: str
    voice_port: int
    secret_key: List[int]
    ssrc: int
    token: Any
    socket: Any
    loop: Any
    mode: Any
    sequence: int
    timestamp: int
    channel: Any
    timeout: int
    encoder: Any
    ws: Any
    def __init__(self, state: ConnectionState, channel: VoiceChannel) -> None: ...
    warn_nacl: Any
    supported_modes: Tuple[str]
    session_id: Any
    async def on_voice_state_update(self, data) -> None: ...
    guild_id: Any
    endpoint: Any
    async def on_voice_server_update(self, data: dict): ...
    async def voice_connect(self) -> None: ...
    async def voice_disconnect(self) -> None: ...
    def prepare_handshake(self) -> None: ...
    def finish_handshake(self) -> None: ...
    async def ws_connect(self) -> VoiceGateway: ...
    async def connect(self, reconnect: bool, timeout: float): ...
    async def watch_voice_ws(self, reconnect: bool): ...
    async def disconnect(self, *, force: bool = ...): ...
    async def move_to(self, channel: int): ...
    def is_connected(self) -> bool: ...
    def checked_add(self, attr, value, limit) -> None: ...
    def send_audio_packet(self, data: bytes, *, encode: bool = ...): ...
