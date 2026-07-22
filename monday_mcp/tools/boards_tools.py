"""Boards group: fetch_boards, fetch_boards_by_id, fetch_all_items_by_board_id,
fetch_item_by_board_id_by_update_date, fetch_columns_by_board_id."""

import dataclasses
import logging
from typing import Any, Mapping, Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.boards import (
    BoardData,
    BoardKind,
    BoardListData,
    BoardListResult,
    BoardResult,
    BoardsOrderBy,
    BoardState,
    ItemListData,
    ItemListResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("monday-mcp.tools.boards")


def register_boards_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="fetch_boards",
        description="Query boards with optional filters.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_boards(
        limit: int = Field(default=50, description="Number of boards to return."),
        page: Optional[int] = Field(default=None, description="Page number for pagination."),
        ids: Optional[list[int]] = Field(default=None, description="Filter by specific board IDs."),
        board_kind: Optional[BoardKind] = Field(
            default=None, description="Filter by board type (public, private, share)."
        ),
        state: Optional[BoardState] = Field(
            default=None, description="Filter by state (active, archived, deleted, all)."
        ),
        order_by: Optional[BoardsOrderBy] = Field(
            default=None, description="Sort order (created_at or used_at)."
        ),
    ) -> BoardListResult:
        tlog = ToolLogger(logger, "fetch_boards")
        try:
            response = service.get_client().boards.fetch_boards(
                limit=limit, page=page, ids=ids, board_kind=board_kind, state=state, order_by=order_by,
            )
            boards = [dataclasses.asdict(b) for b in (response.data.boards or [])]
            tlog.success()
            return BoardListResult(
                success=True, statusCode=200,
                data=BoardListData(boards=[BoardData(**b) for b in boards]),
            )
        except Exception as exc:
            return _handle_request_exc(BoardListResult, tlog, exc)

    @mcp.tool(
        name="fetch_boards_by_id",
        description="Fetch a single board by ID.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_boards_by_id(
        board_id: str = Field(..., description="Board Id"),
    ) -> BoardResult:
        tlog = ToolLogger(logger, "fetch_boards_by_id")
        try:
            response = service.get_client().boards.fetch_boards_by_id(board_id=board_id)
            boards = response.data.boards or []
            if not boards:
                return _err(BoardResult, tlog, "NOT_FOUND", f"Board {board_id} not found", 404)
            tlog.success()
            return BoardResult(
                success=True, statusCode=200,
                data=BoardData(**dataclasses.asdict(boards[0])),
            )
        except Exception as exc:
            return _handle_request_exc(BoardResult, tlog, exc)

    @mcp.tool(
        name="fetch_all_items_by_board_id",
        description="Fetch all items with automatic pagination.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_all_items_by_board_id(
        board_id: int | str = Field(..., description="The board ID to fetch items from."),
        query_params: Optional[Mapping[str, Any]] = Field(default=None, description="Query Params for filtering"),
        limit: Optional[int] = Field(default=None, description="Number of items per page"),
    ) -> ItemListResult:
        tlog = ToolLogger(logger, "fetch_all_items_by_board_id")
        try:
            items = service.get_client().boards.fetch_all_items_by_board_id(
                board_id=board_id, query_params=query_params, limit=limit,
            )
            tlog.success()
            return ItemListResult(
                success=True, statusCode=200,
                data=ItemListData(items=[dataclasses.asdict(i) for i in items]),
            )
        except Exception as exc:
            return _handle_request_exc(ItemListResult, tlog, exc)

    @mcp.tool(
        name="fetch_item_by_board_id_by_update_date",
        description="Fetch items modified within a date range.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_item_by_board_id_by_update_date(
        board_id: int | str = Field(..., description="The board ID to fetch items from."),
        updated_after: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
        updated_before: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
    ) -> ItemListResult:
        tlog = ToolLogger(logger, "fetch_item_by_board_id_by_update_date")
        try:
            items = service.get_client().boards.fetch_item_by_board_id_by_update_date(
                board_id=board_id, updated_after=updated_after, updated_before=updated_before,
            )
            tlog.success()
            return ItemListResult(
                success=True, statusCode=200,
                data=ItemListData(items=[dataclasses.asdict(i) for i in items]),
            )
        except Exception as exc:
            return _handle_request_exc(ItemListResult, tlog, exc)

    @mcp.tool(
        name="fetch_columns_by_board_id",
        description="Useful for incremental syncing — only fetch items modified within a date range.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_columns_by_board_id(
        board_id: str = Field(..., description="board id"),
    ) -> BoardResult:
        tlog = ToolLogger(logger, "fetch_columns_by_board_id")
        try:
            response = service.get_client().boards.fetch_columns_by_board_id(board_id=board_id)
            boards = response.data.boards or []
            if not boards:
                return _err(BoardResult, tlog, "NOT_FOUND", f"Board {board_id} not found", 404)
            tlog.success()
            return BoardResult(
                success=True, statusCode=200,
                data=BoardData(**dataclasses.asdict(boards[0])),
            )
        except Exception as exc:
            return _handle_request_exc(BoardResult, tlog, exc)
