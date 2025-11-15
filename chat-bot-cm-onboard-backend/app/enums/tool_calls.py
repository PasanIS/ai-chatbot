from enum import Enum


class ToolCalls(str, Enum):
    DATABASE_QUERY = "database_query_tool"
    WEB_SEARCH = "web_search_tool"