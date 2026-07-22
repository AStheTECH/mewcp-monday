"""Items group: create_item, create_subitem, change_simple_column_value,
change_status_column_value, change_date_column_value, change_custom_column_value,
change_multiple_column_values, move_item_to_group, archive_item_by_id,
delete_item_by_id, upload_file_to_column, fetch_items_by_column_value,
fetch_items_by_id."""

import dataclasses
import logging
from datetime import datetime
from typing import Any, Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.items import (
    ColumnChangeData,
    ColumnChangeResult,
    ColumnValuesChangeData,
    ColumnValuesChangeResult,
    CreatedItemData,
    CreatedItemResult,
    FileUploadData,
    FileUploadResult,
    ItemIdData,
    ItemIdResult,
    ItemListData,
    ItemListResult,
    ItemPageData,
    ItemPageResult,
    SubitemData,
    SubitemResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("monday-mcp.tools.items")


def register_items_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_item",
        description="Creating an Item",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_item(
        board_id: int | str = Field(..., description="The board ID to fetch items from."),
        group_id: int | str = Field(..., description="The board ID to fetch items from."),
        item_name: str = Field(..., description="Name of Item"),
        column_values: Optional[dict[str, Any]] = Field(
            default=None, description="The column values of the new item."
        ),
        create_labels_if_missing: Optional[bool] = Field(
            default=False,
            description="Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)",
        ),
    ) -> CreatedItemResult:
        tlog = ToolLogger(logger, "create_item")
        try:
            response = service.get_client().items.create_item(
                board_id=board_id, group_id=group_id, item_name=item_name,
                column_values=column_values, create_labels_if_missing=create_labels_if_missing,
            )
            created = response.data.create_item
            tlog.success()
            return CreatedItemResult(
                success=True, statusCode=200,
                data=CreatedItemData(**dataclasses.asdict(created)) if created else CreatedItemData(),
            )
        except Exception as exc:
            return _handle_request_exc(CreatedItemResult, tlog, exc)

    @mcp.tool(
        name="create_subitem",
        description="Create a subitem",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_subitem(
        parent_item_id: int | str = Field(..., description="The parent item's unique identifier."),
        subitem_name: str = Field(..., description="The new item's name."),
        column_values: Optional[dict[str, Any]] = Field(
            default=None, description="The column values of the new item."
        ),
        create_labels_if_missing: Optional[bool] = Field(
            default=False,
            description="Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)",
        ),
    ) -> SubitemResult:
        tlog = ToolLogger(logger, "create_subitem")
        try:
            response = service.get_client().items.create_subitem(
                parent_item_id=parent_item_id, subitem_name=subitem_name,
                column_values=column_values, create_labels_if_missing=create_labels_if_missing,
            )
            raw = response.response_data["data"]["create_subitem"]
            tlog.success()
            return SubitemResult(success=True, statusCode=200, data=SubitemData(**raw))
        except Exception as exc:
            return _handle_request_exc(SubitemResult, tlog, exc)

    @mcp.tool(
        name="change_simple_column_value",
        description="Change an item's column with simple value.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def change_simple_column_value(
        board_id: int | str = Field(..., description="The board's unique identifier."),
        item_id: int | str = Field(..., description="The item's unique identifier."),
        column_id: str = Field(..., description="The column's unique identifier."),
        value: str = Field(..., description="The new simple value of the column (pass null to empty the column)."),
    ) -> ItemIdResult:
        tlog = ToolLogger(logger, "change_simple_column_value")
        try:
            response = service.get_client().items.change_simple_column_value(
                board_id=board_id, item_id=item_id, column_id=column_id, value=value,
            )
            raw = response.response_data["data"]["change_simple_column_value"]
            tlog.success()
            return ItemIdResult(success=True, statusCode=200, data=ItemIdData(**raw))
        except Exception as exc:
            return _handle_request_exc(ItemIdResult, tlog, exc)

    @mcp.tool(
        name="change_status_column_value",
        description="Set a status column's label.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def change_status_column_value(
        board_id: int | str = Field(..., description="The board's unique identifier."),
        item_id: int | str = Field(..., description="The item's unique identifier."),
        column_id: str = Field(..., description="The column's unique identifier."),
        value: str = Field(..., description="The new simple value of the column (pass null to empty the column)."),
    ) -> ColumnChangeResult:
        tlog = ToolLogger(logger, "change_status_column_value")
        try:
            response = service.get_client().items.change_status_column_value(
                board_id=board_id, item_id=item_id, column_id=column_id, value=value,
            )
            raw = response.response_data["data"]["change_column_value"]
            tlog.success()
            return ColumnChangeResult(success=True, statusCode=200, data=ColumnChangeData(**raw))
        except Exception as exc:
            return _handle_request_exc(ColumnChangeResult, tlog, exc)

    @mcp.tool(
        name="change_date_column_value",
        description="Set a date column's value (pass a datetime object)",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def change_date_column_value(
        board_id: int | str = Field(..., description="The board's unique identifier."),
        item_id: int | str = Field(..., description="The item's unique identifier."),
        column_id: str = Field(..., description="The column's unique identifier."),
        timestamp: datetime = Field(..., description="The new date value"),
    ) -> ColumnChangeResult:
        tlog = ToolLogger(logger, "change_date_column_value")
        try:
            response = service.get_client().items.change_date_column_value(
                board_id=board_id, item_id=item_id, column_id=column_id, timestamp=timestamp,
            )
            raw = response.response_data["data"]["change_column_value"]
            tlog.success()
            return ColumnChangeResult(success=True, statusCode=200, data=ColumnChangeData(**raw))
        except Exception as exc:
            return _handle_request_exc(ColumnChangeResult, tlog, exc)

    @mcp.tool(
        name="change_custom_column_value",
        description="Set any column's value using a JSON dict.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def change_custom_column_value(
        board_id: int | str = Field(..., description="The board's unique identifier."),
        item_id: int | str = Field(..., description="The item's unique identifier."),
        column_id: str = Field(..., description="The column's unique identifier."),
        value: dict[str, Any] = Field(
            ..., description="The new value of the column as a JSON dict (e.g. {'checked': True} for a checkbox)."
        ),
    ) -> ColumnChangeResult:
        tlog = ToolLogger(logger, "change_custom_column_value")
        try:
            response = service.get_client().items.change_custom_column_value(
                board_id=board_id, item_id=item_id, column_id=column_id, value=value,
            )
            raw = response.response_data["data"]["change_column_value"]
            tlog.success()
            return ColumnChangeResult(success=True, statusCode=200, data=ColumnChangeData(**raw))
        except Exception as exc:
            return _handle_request_exc(ColumnChangeResult, tlog, exc)

    @mcp.tool(
        name="change_multiple_column_values",
        description="Set multiple column values at once.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def change_multiple_column_values(
        board_id: int | str = Field(..., description="The board's unique identifier."),
        item_id: int | str = Field(..., description="The item's unique identifier."),
        column_values: dict[str, Any] = Field(..., description="Column values in a json format"),
        create_labels_if_missing: Optional[bool] = Field(
            default=False,
            description="Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)",
        ),
    ) -> ColumnValuesChangeResult:
        tlog = ToolLogger(logger, "change_multiple_column_values")
        try:
            response = service.get_client().items.change_multiple_column_values(
                board_id=board_id, item_id=item_id, column_values=column_values,
                create_labels_if_missing=create_labels_if_missing,
            )
            raw = response.response_data["data"]["change_multiple_column_values"]
            tlog.success()
            return ColumnValuesChangeResult(success=True, statusCode=200, data=ColumnValuesChangeData(**raw))
        except Exception as exc:
            return _handle_request_exc(ColumnValuesChangeResult, tlog, exc)

    @mcp.tool(
        name="move_item_to_group",
        description="Move an item to a different group.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def move_item_to_group(
        item_id: int = Field(..., description="The item's unique identifier."),
        group_id: str = Field(..., description="The group's unique identifier."),
    ) -> ItemIdResult:
        tlog = ToolLogger(logger, "move_item_to_group")
        try:
            response = service.get_client().items.move_item_to_group(item_id=item_id, group_id=group_id)
            raw = response.response_data["data"]["move_item_to_group"]
            tlog.success()
            return ItemIdResult(success=True, statusCode=200, data=ItemIdData(**raw))
        except Exception as exc:
            return _handle_request_exc(ItemIdResult, tlog, exc)

    @mcp.tool(
        name="archive_item_by_id",
        description=(
            "Archives an item, removing it from active board views. "
            "Unlike delete, this is REVERSIBLE — the item can be restored from Monday.com's "
            "archive. Confirm with the user before calling, since it changes the item's "
            "visibility across the board."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def archive_item_by_id(
        item_id: int = Field(..., description="The item's unique identifier."),
    ) -> ItemIdResult:
        tlog = ToolLogger(logger, "archive_item_by_id")
        try:
            response = service.get_client().items.archive_item_by_id(item_id=item_id)
            raw = response.response_data["data"]["archive_item"]
            tlog.success()
            return ItemIdResult(success=True, statusCode=200, data=ItemIdData(**raw))
        except Exception as exc:
            return _handle_request_exc(ItemIdResult, tlog, exc)

    @mcp.tool(
        name="delete_item_by_id",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently deletes the item and all its data (column values, subitems, updates). "
            "This action is irreversible — the item and its data cannot be recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_item_by_id(
        item_id: int = Field(..., description="The item's unique identifier."),
    ) -> ItemIdResult:
        tlog = ToolLogger(logger, "delete_item_by_id")
        try:
            response = service.get_client().items.delete_item_by_id(item_id=item_id)
            raw = response.response_data["data"]["delete_item"]
            tlog.success()
            return ItemIdResult(success=True, statusCode=200, data=ItemIdData(**raw))
        except Exception as exc:
            return _handle_request_exc(ItemIdResult, tlog, exc)

    @mcp.tool(
        name="upload_file_to_column",
        description="Upload a file to a file column.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def upload_file_to_column(
        item_id: int | str = Field(..., description="The item's unique identifier."),
        column_id: str = Field(..., description="The column's unique identifier."),
        file_path: str = Field(..., description="The path of the file on the user's system"),
        mimetype: Optional[str] = Field(
            default=None, description="The mimetype of the file getting uploaded for example: application/json"
        ),
    ) -> FileUploadResult:
        tlog = ToolLogger(logger, "upload_file_to_column")
        try:
            response = service.get_client().items.upload_file_to_column(
                item_id=item_id, column_id=column_id, file_path=file_path, mimetype=mimetype,
            )
            if "errors" in response:
                return _err(FileUploadResult, tlog, "UPSTREAM_ERROR", str(response["errors"]), 502)
            raw = response["data"]["add_file_to_column"]
            tlog.success()
            return FileUploadResult(success=True, statusCode=200, data=FileUploadData(**raw))
        except Exception as exc:
            return _handle_request_exc(FileUploadResult, tlog, exc)

    @mcp.tool(
        name="fetch_items_by_column_value",
        description="Fetch items by column value",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_items_by_column_value(
        board_id: int | str = Field(..., description="Board Id"),
        column_id: str = Field(..., description="column header"),
        value: str = Field(..., description="Fetch column by this value"),
        limit: Optional[int] = Field(default=None, description="Limit on number of rows to be fetched"),
    ) -> ItemPageResult:
        tlog = ToolLogger(logger, "fetch_items_by_column_value")
        try:
            response = service.get_client().items.fetch_items_by_column_value(
                board_id=board_id, column_id=column_id, value=value, limit=limit,
            )
            page = response.data.items_page_by_column_values
            items = [dataclasses.asdict(i) for i in (page.items or [])] if page else []
            cursor = page.cursor if page else None
            tlog.success()
            return ItemPageResult(success=True, statusCode=200, data=ItemPageData(cursor=cursor, items=items))
        except Exception as exc:
            return _handle_request_exc(ItemPageResult, tlog, exc)

    @mcp.tool(
        name="fetch_items_by_id",
        description="Fetch items by a list of ids",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_items_by_id(
        ids: list[int | str] = Field(..., description="list of ids for the items to be fetched"),
    ) -> ItemListResult:
        tlog = ToolLogger(logger, "fetch_items_by_id")
        try:
            items = service.get_client().items.fetch_items_by_id(ids=ids)
            tlog.success()
            return ItemListResult(
                success=True, statusCode=200,
                data=ItemListData(items=[dataclasses.asdict(i) for i in (items or [])]),
            )
        except Exception as exc:
            return _handle_request_exc(ItemListResult, tlog, exc)
