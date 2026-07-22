"""Updates group: create_update, delete_update, fetch_updates,
fetch_updates_for_item, fetch_board_updates, fetch_board_updates_page."""

import dataclasses
import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.updates import (
    ItemUpdateData,
    ItemUpdateListData,
    ItemUpdateListResult,
    SimpleUpdateData,
    SimpleUpdateListData,
    SimpleUpdateListResult,
    UpdateData,
    UpdateIdData,
    UpdateIdResult,
    UpdateListData,
    UpdateListResult,
)
from ._helpers import _handle_request_exc

logger = logging.getLogger("monday-mcp.tools.updates")


def register_updates_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_update",
        description="Create an update (comment) on an item.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_update(
        item_id: int = Field(..., description="The item's unique identifier."),
        update_value: str = Field(..., description="Comments to be added to the item"),
    ) -> UpdateIdResult:
        tlog = ToolLogger(logger, "create_update")
        try:
            response = service.get_client().updates.create_update(
                item_id=item_id, update_value=update_value,
            )
            created = response.response_data["data"]["create_update"]
            tlog.success()
            return UpdateIdResult(
                success=True, statusCode=200,
                data=UpdateIdData(**created),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateIdResult, tlog, exc)

    @mcp.tool(
        name="delete_update",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently deletes an update (comment) from an item. "
            "This action is irreversible — the update's content cannot be recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_update(
        item_id: int = Field(..., description="The item's unique identifier."),
    ) -> UpdateIdResult:
        tlog = ToolLogger(logger, "delete_update")
        try:
            response = service.get_client().updates.delete_update(item_id=item_id)
            deleted = response.response_data["data"]["delete_update"]
            tlog.success()
            return UpdateIdResult(
                success=True, statusCode=200,
                data=UpdateIdData(**deleted),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateIdResult, tlog, exc)

    @mcp.tool(
        name="fetch_updates",
        description="Fetch updates with pagination.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_updates(
        limit: int = Field(..., description="Number of items to get, the default is 25."),
        page: int = Field(..., description="Page number to get, starting at 1."),
    ) -> SimpleUpdateListResult:
        tlog = ToolLogger(logger, "fetch_updates")
        try:
            response = service.get_client().updates.fetch_updates(limit=limit, page=page)
            updates = response.response_data["data"]["updates"]
            tlog.success()
            return SimpleUpdateListResult(
                success=True, statusCode=200,
                data=SimpleUpdateListData(updates=[SimpleUpdateData(**u) for u in updates]),
            )
        except Exception as exc:
            return _handle_request_exc(SimpleUpdateListResult, tlog, exc)

    @mcp.tool(
        name="fetch_updates_for_item",
        description="Fetch updates for a specific item.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_updates_for_item(
        item_id: int = Field(..., description="The item's unique identifier."),
        limit: int = Field(..., description="Number of items to get, the default is 25."),
    ) -> ItemUpdateListResult:
        tlog = ToolLogger(logger, "fetch_updates_for_item")
        try:
            response = service.get_client().updates.fetch_updates_for_item(
                item_id=item_id, limit=limit,
            )
            items = response.response_data["data"]["items"]
            updates = items[0]["updates"] if items else []
            tlog.success()
            return ItemUpdateListResult(
                success=True, statusCode=200,
                data=ItemUpdateListData(updates=[ItemUpdateData(**u) for u in updates]),
            )
        except Exception as exc:
            return _handle_request_exc(ItemUpdateListResult, tlog, exc)

    @mcp.tool(
        name="fetch_board_updates",
        description="Fetch all updates from a board with date filtering.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_board_updates(
        board_ids: int = Field(..., description="Board Id"),
        updated_after: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
        updated_before: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
    ) -> UpdateListResult:
        tlog = ToolLogger(logger, "fetch_board_updates")
        try:
            updates = service.get_client().updates.fetch_board_updates(
                board_ids=board_ids, updated_after=updated_after, updated_before=updated_before,
            )
            tlog.success()
            return UpdateListResult(
                success=True, statusCode=200,
                data=UpdateListData(updates=[UpdateData(**dataclasses.asdict(u)) for u in updates]),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateListResult, tlog, exc)

    @mcp.tool(
        name="fetch_board_updates_page",
        description="Fetch a single page of board updates.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_board_updates_page(
        board_id: int | str = Field(..., description="Board Id"),
        limit: int = Field(..., description="Number of items to get, the default is 25."),
        page: int = Field(..., description="Page number to get, starting at 1."),
        from_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
        to_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
    ) -> UpdateListResult:
        tlog = ToolLogger(logger, "fetch_board_updates_page")
        try:
            updates = service.get_client().updates.fetch_board_updates_page(
                board_id=board_id, limit=limit, page=page, from_date=from_date, to_date=to_date,
            )
            tlog.success()
            return UpdateListResult(
                success=True, statusCode=200,
                data=UpdateListData(updates=[UpdateData(**dataclasses.asdict(u)) for u in updates]),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateListResult, tlog, exc)
