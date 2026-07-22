"""Activity logs group schemas: fetch_activity_logs_from_board,
fetch_all_activity_logs_from_board."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ActivityLogData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    account_id: str
    created_at: str
    data: str
    entity: str
    event: str
    user_id: str


class ActivityLogListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    activity_logs: list[ActivityLogData]


class ActivityLogListResult(ToolResult):
    data: ActivityLogListData | None = None
