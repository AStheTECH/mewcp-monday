"""Activity logs group: fetch_activity_logs_from_board, fetch_all_activity_logs_from_board."""

import dataclasses
import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.activity_logs import ActivityLogData, ActivityLogListData, ActivityLogListResult
from ._helpers import _handle_request_exc

logger = logging.getLogger("monday-mcp.tools.activity_logs")


def register_activity_logs_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="fetch_activity_logs_from_board",
        description="Fetch a page of activity logs.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_activity_logs_from_board(
        board_ids: int = Field(..., description="Board Id"),
        page: int = Field(..., description="Page number to get, starting at 1."),
        limit: int = Field(..., description="Number of items to get, the default is 25."),
        from_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
        to_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
    ) -> ActivityLogListResult:
        tlog = ToolLogger(logger, "fetch_activity_logs_from_board")
        try:
            response = service.get_client().activity_logs.fetch_activity_logs_from_board(
                board_ids=board_ids, page=page, limit=limit, from_date=from_date, to_date=to_date,
            )
            logs = response.data.boards[0].activity_logs
            tlog.success()
            return ActivityLogListResult(
                success=True, statusCode=200,
                data=ActivityLogListData(
                    activity_logs=[ActivityLogData(**dataclasses.asdict(log)) for log in logs]
                ),
            )
        except Exception as exc:
            return _handle_request_exc(ActivityLogListResult, tlog, exc)

    @mcp.tool(
        name="fetch_all_activity_logs_from_board",
        description="Fetch all activity logs with automatic pagination and optional event filtering.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def fetch_all_activity_logs_from_board(
        board_ids: int = Field(..., description="Board Id"),
        from_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
        to_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ"),
        limit: int = Field(..., description="Number of items to get, the default is 25."),
        events_filter: list[str] = Field(..., description="Filter activity logs by specific event types"),
    ) -> ActivityLogListResult:
        tlog = ToolLogger(logger, "fetch_all_activity_logs_from_board")
        try:
            logs = service.get_client().activity_logs.fetch_all_activity_logs_from_board(
                board_ids=board_ids, from_date=from_date, to_date=to_date,
                limit=limit, events_filter=events_filter,
            )
            tlog.success()
            return ActivityLogListResult(
                success=True, statusCode=200,
                data=ActivityLogListData(
                    activity_logs=[ActivityLogData(**dataclasses.asdict(log)) for log in logs]
                ),
            )
        except Exception as exc:
            return _handle_request_exc(ActivityLogListResult, tlog, exc)
