class Enum:
    def __new__(self, name, value) -> None: ...

class ButtonStyle(Enum):
    PRIMARY: int
    SECONDARY: int
    SUCCESS: int
    DANGER: int
    LINK: int
    BLURPLE: int
    GRAY: int
    GREEN: int
    RED: int

class ChannelType(Enum):
    GUILD_TEXT: int
    DM: int
    GUILD_VOICE: int
    GROUP_DM: int
    GUILD_CATEGORY: int
    GUILD_NEWS: int
    GUILD_STORE: int
    GUILD_NEWS_THREAD: int
    GUILD_PUBLIC_THREAD: int
    GUILD_PRIVATE_THREAD: int
    GUILD_STAGE_VOICE: int

class VideoQuality(Enum):
    AUTO: int
    FULL: int

class ApplicationCommandType(Enum):
    CHAT_INPUT: int
    USER: int
    MESSAGE: int

class StickerType(Enum):
    STANDARD: int
    GUILD: int

class StickerFormatType(Enum):
    PNG: int
    APNG: int
    LOTTIE: int

class FormatType(Enum):
    JPEG: str
    PNG: str
    WEBP: str
    GIF: str
    LOTTIE: str

class ScheduledEventStatusType(Enum):
    SCHEDULED: int
    ACTIVE: int
    COMPLETED: int
    CANCELED: int

class ScheduledEventType(Enum):
    STAGE_INSTANCE: int
    VOICE: int
    EXTERNAL: int
