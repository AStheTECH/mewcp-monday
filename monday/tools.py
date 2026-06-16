import logging
from pydantic import Field
from fastmcp import FastMCP
from typing import List
import json
from .schemas import (
    FetchBoardsQueryParams,
    FetchItemsQueryParams,
    FetchItemsByUpdateDateQueryParams,
    CreateItemQueryParams,
    CreateSubitemQueryParams,
    ChangeColumnQueryParams,
    ChangeDateColumnQueryParams,
    ChangeMultipleColumnQueryParams,
    MoveItemQueryParams,
    UploadFileQueryParams,
    UpdateQueryParams,
    FetchUpdateQueryParams,
    FetchUpdatesForItemsQueryParams,
    FetchBoardUpdatesQueryParams,
    FetchBoardUpdatestPageQueryParams,
    FetchActivityLogsFromBoardQueryParams,
    FetchAllActivityLogsQueryParams,
    FetchItemsByColumnQueryParams,
    ApiObjectResponse
)
from .service import get_client

logger = logging.getLogger("calendar-mcp-server")


class _ToolCollector:
    def __init__(self):
        self.items = []

    def tool(self, *args, **kwargs):
        def decorator(func):
            self.items.append((args, kwargs, func))
            return func

        return decorator


mcp = _ToolCollector()


def register_tools(real_mcp: FastMCP) -> None:
    for args, kwargs, func in mcp.items:
        real_mcp.tool(*args, **kwargs)(func)


@mcp.tool(
    name="fetch_boards",
    description="Query boards with optional filters."
)
def fetch_boards(params: FetchBoardsQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().boards.fetch_boards(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching boards: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_boards_by_id",
    description="Fetch a single board by ID."
)
def fetch_boards_by_id(board_id: str = Field(..., description="Board Id")) -> ApiObjectResponse:
    try:
        response = get_client().boards.fetch_boards_by_id(board_id=board_id)
        return response
    except Exception as exc:
        logging.error(f"Error fetching board: {exc}", exc_info=True)
        return {"error": str(exc)}



@mcp.tool(
    name="fetch_all_items_by_board_id",
    description="Fetch all items with automatic pagination."
)
def fetch_all_items_by_board_id(params: FetchItemsQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().boards.fetch_all_items_by_board_id(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching items: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_item_by_board_id_by_update_date",
    description="Fetch items modified within a date range."
)
def fetch_item_by_board_id_by_update_date(params: FetchItemsByUpdateDateQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().boards.fetch_item_by_board_id_by_update_date(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching item: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_columns_by_board_id",
    description="Useful for incremental syncing — only fetch items modified within a date range."
)
def fetch_columns_by_board_id(board_id: str = Field(..., description="board id")) -> ApiObjectResponse:
    try:
        response = get_client().boards.fetch_columns_by_board_id(board_id=board_id)
        return response
    except Exception as exc:
        logging.error(f"Error fetching columns: {exc}", exc_info=True)
        return {"error": str(exc)}


@mcp.tool(
    name="create_item",
    description="Creating an Item"
)
def create_item(params: CreateItemQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.create_item(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error creating item: {exc}", exc_info=True)
        return {"error": str(exc)}


@mcp.tool(
    name="create_subitem",
    description="Create a subitem"
)
def create_subitem(params: CreateSubitemQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.create_subitem(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error creating subitem: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="change_simple_column_value",
    description="Change an item's column with simple value."
)
def change_simple_column_value(params: ChangeColumnQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.change_simple_column_value(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error changing column value: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="change_status_column_value",
    description="Set a status column's label."
)
def change_status_column_value(params: ChangeColumnQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.change_status_column_value(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error changing column value: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="change_date_column_value",
    description="Set a date column's value (pass a datetime object)"
)
def change_date_column_value(params: ChangeDateColumnQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.change_date_column_value(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error changing column value: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="change_custom_column_value",
    description="Set any column's value using a JSON dict."
)
def change_custom_column_value(params: ChangeColumnQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.change_custom_column_value(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error changing column value: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="change_multiple_column_values",
    description="Set multiple column values at once."
)
def change_multiple_column_values(params: ChangeMultipleColumnQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.change_multiple_column_values(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error changing column values: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="move_item_to_group",
    description="Move an item to a different group."
)
def move_item_to_group(params: MoveItemQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.move_item_to_group(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error moving item to the new group: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="archive_item_by_id",
    description="Archive an item."
)
def archive_item_by_id(item_id: int = Field(..., description="The item's unique identifier.")) -> ApiObjectResponse:
    try:
        response = get_client().items.archive_item_by_id(item_id=item_id)
        return response
    except Exception as exc:
        logging.error(f"Error archiving the item: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="delete_item_by_id",
    description="Permanently delete an item."
)
def delete_item_by_id(item_id: int = Field(..., description="The item's unique identifier.")) -> ApiObjectResponse:
    try:
        response = get_client().items.delete_item_by_id(item_id=item_id)
        return response
    except Exception as exc:
        logging.error(f"Error deleting the item: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="upload_file_to_column",
    description="Upload a file to a file column."
)
def upload_file_to_column(params: UploadFileQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.upload_file_to_column(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error uploading file to the column: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="create_update",
    description="Create an update (comment) on an item."
)
def create_update(params: UpdateQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().updates.create_update(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error creating updates to the item: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="delete_update",
    description="Delete an update."
)
def delete_update(item_id: int = Field(..., description="The item's unique identifier.")) -> ApiObjectResponse:
    try:
        response = get_client().updates.delete_update(item_id=item_id)
        return response
    except Exception as exc:
        logging.error(f"Error deleting updates from the item: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_updates",
    description="Fetch updates with pagination"
)
def fetch_updates(params: FetchUpdateQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().updates.fetch_updates(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching updates to the item: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_updates_for_item",
    description="Fetch updates for a specific item."
)
def fetch_updates_for_item(params: FetchUpdatesForItemsQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().updates.fetch_updates_for_item(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetch updates to the item: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_board_updates",
    description="Fetch all updates from a board with date filtering."
)
def fetch_board_updates(params: FetchBoardUpdatesQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().updates.fetch_board_updates(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching board updates: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_board_updates_page",
    description="Fetch a single page of board updates."
)
def fetch_board_updates_page(params: FetchBoardUpdatestPageQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().updates.fetch_board_updates_page(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching board update pages: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_activity_logs_from_board",
    description="etch a page of activity logs."
)
def fetch_activity_logs_from_board(params: FetchActivityLogsFromBoardQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().activity_logs.fetch_activity_logs_from_board(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching activity logs from board: {exc}", exc_info=True)
        return {"error": str(exc)}


@mcp.tool(
    name="fetch_all_activity_logs_from_board",
    description="Fetch all activity logs with automatic pagination and optional event filtering."
)
def fetch_all_activity_logs_from_board(params: FetchAllActivityLogsQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().activity_logs.fetch_all_activity_logs_from_board(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching activity logs from board: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="get_document_with_blocks",
    description="Fetch a document with all blocks (auto-paginates)."
)
def get_document_with_blocks(doc_id: str = Field(..., description="doc id")) -> ApiObjectResponse:
    try:
        response = get_client().docs.get_document_with_blocks(doc_id=doc_id)
        return response or {}
    except Exception as exc:
        logging.error(f"Error fetching document: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_items_by_column_value",
    description="Fetch items by column value"
)
def fetch_items_by_column_value(params: FetchItemsByColumnQueryParams) -> ApiObjectResponse:
    try:
        response = get_client().items.fetch_items_by_column_value(**params.model_dump())
        return response
    except Exception as exc:
        logging.error(f"Error fetching items by column value: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="fetch_items_by_id",
    description="Fetch items by a list of ids"
)
def fetch_items_by_id(ids: List[int | str] = Field(..., description="list of ids for the items to be fetched")) -> ApiObjectResponse:
    try:
        response = get_client().items.fetch_items_by_id(ids=ids)
        return response
    except Exception as exc:
        logging.error(f"Error fetching items by ids: {exc}", exc_info=True)
        return {"error": str(exc)}

@mcp.tool(
    name="monday_health_check",
    description="Check server readiness and basic connectivity.",
)
def google_search_console_health_check() -> str:
    """Health check endpoint."""
    return json.dumps(
        {
            "status": "ok",
            "server": "Monday.com MCP Server",
            "type": "third-party integration",
            "auth_required": "oauth token required",
        }
    )



