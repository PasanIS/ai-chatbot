from enum import Enum


class Roles(str, Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"