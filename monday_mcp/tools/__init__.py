"""MewCP Monday.com tool registration."""

from fastmcp import FastMCP

from .activity_logs_tools import register_activity_logs_tools
from .boards_tools import register_boards_tools
from .docs_tools import register_docs_tools
from .items_tools import register_items_tools
from .system_tools import register_system_tools
from .updates_tools import register_updates_tools


def register_tools(mcp: FastMCP) -> None:
    register_boards_tools(mcp)
    register_items_tools(mcp)
    register_updates_tools(mcp)
    register_activity_logs_tools(mcp)
    register_docs_tools(mcp)
    register_system_tools(mcp)
