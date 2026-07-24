"""Configuration for MewCP Monday MCP Server."""

import logging
import os

SERVER_VERSION = "v1.0.0"
BREAKING_CHANGES: list[dict] = []

# OAuth scopes this server's tools require, per monday.com's documented scope set
# (https://auth.monday.com/oauth_ms/.well-known/oauth-authorization-server).
# boards:read   — fetch_boards, fetch_boards_by_id, fetch_columns_by_board_id,
#                 fetch_activity_logs_from_board, fetch_all_activity_logs_from_board
#                 (activity logs are nested under boards{activity_logs{...}} — no separate scope)
# items:read    — fetch_all_items_by_board_id, fetch_item_by_board_id_by_update_date,
#                 fetch_items_by_column_value, fetch_items_by_id
# items:write   — create_item, create_subitem, change_simple_column_value,
#                 change_status_column_value, change_date_column_value,
#                 change_custom_column_value, change_multiple_column_values,
#                 move_item_to_group, archive_item_by_id, delete_item_by_id,
#                 upload_file_to_column
# updates:read  — fetch_updates, fetch_updates_for_item, fetch_board_updates,
#                 fetch_board_updates_page
# updates:write — create_update, delete_update
# docs:read     — get_document_with_blocks
SCOPES = [
    "boards:read",
    "items:read",
    "items:write",
    "updates:read",
    "updates:write",
    "docs:read",
]


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
