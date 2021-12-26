from typing import Any, Optional, TypedDict

from .snowflake import Snowflake as Snowflake

class PartialUser(TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: Optional[str]

PremiumType: Any

class User(PartialUser):
    bot: bool
    system: bool
    mfa_enabled: bool
    local: str
    verified: bool
    email: Optional[str]
    flags: int
    premium_type: PremiumType
    public_flags: int
