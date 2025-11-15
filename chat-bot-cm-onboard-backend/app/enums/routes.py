from enum import Enum


class Routes(str, Enum):
    NORMAL_CHAT = "normal_chat"
    TOOL_CALL = "tool_call"