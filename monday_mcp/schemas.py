from enum import Enum
from typing import Any, Optional, TypedDict, Mapping, Dict, List
from monday_sdk import MondayApiResponse, Item, Update, ActivityLog, Document
from pydantic import BaseModel, Field
from datetime import datetime


class ToolError(TypedDict):
    error: str

ApiObjectResponse = MondayApiResponse | List[Item] | List[Update] | List[ActivityLog] | Document | dict | ToolError


class BoardKind(str, Enum):
    public = "public"
    private = "private"
    share = "share"


class BoardState(str, Enum):
    active = "active"
    archived = "archived"
    deleted = "deleted"
    all = "all"


class BoardsOrderBy(str, Enum):
    created_at = "created_at"
    used_at = "used_at"


class FetchBoardsQueryParams(BaseModel):
    limit: int = Field(default=50, description="Number of boards to return.")
    page: Optional[int] = Field(default=None, description="Page number for pagination.")
    ids: Optional[list[int]] = Field(default=None, description="Filter by specific board IDs.")
    board_kind: Optional[BoardKind] = Field(
        default=None, description="Filter by board type (public, private, share)."
    )
    state: Optional[BoardState] = Field(
        default=None, description="Filter by state (active, archived, deleted, all)."
    )
    order_by: Optional[BoardsOrderBy] = Field(
        default=None, description="Sort order (created_at or used_at)."
    )

class FetchItemsQueryParams(BaseModel):
    board_id: int | str = Field(..., description="The board ID to fetch items from.")
    query_params: Optional[Mapping[str, Any]] = Field(default=None, description="Query Params for filtering")
    limit: Optional[int] = Field(default=None, description="Number of items per page")

class FetchItemsByUpdateDateQueryParams(BaseModel):
    board_id: int | str = Field(..., description="The board ID to fetch items from.")
    updated_after: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")
    updated_before: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")

class CreateItemQueryParams(BaseModel):
    board_id: int | str = Field(..., description="The board ID to fetch items from.")
    group_id: int | str = Field(..., description="The board ID to fetch items from.")
    item_name: str = Field(..., description="Name of Item")
    column_values: Optional[Dict[str, Any]] = Field(default=None, description="The column values of the new item.")
    create_labels_if_missing: Optional[bool] = Field(default=False, description="Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)")

class CreateSubitemQueryParams(BaseModel):
    parent_item_id: int | str = Field(..., description="The parent item's unique identifier.")
    subitem_name: str = Field(..., description="The new item's name.")
    column_values: Optional[Dict[str, Any]] = Field(default=None, description="The column values of the new item.")
    create_labels_if_missing: Optional[bool] = Field(default=False, description="Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)")

class ChangeColumnQueryParams(BaseModel):
    board_id: int | str = Field(..., description="The board's unique identifier.")
    item_id: int | str = Field(..., description="The item's unique identifier.")
    column_id: str = Field(..., description="The column's unique identifier.")
    value: str = Field(..., description="The new simple value of the column (pass null to empty the column).")

class ChangeCustomColumnQueryParams(BaseModel):
    board_id: int | str = Field(..., description="The board's unique identifier.")
    item_id: int | str = Field(..., description="The item's unique identifier.")
    column_id: str = Field(..., description="The column's unique identifier.")
    value: Dict[str, Any] = Field(..., description="The new value of the column as a JSON dict (e.g. {'checked': True} for a checkbox).")

class ChangeDateColumnQueryParams(BaseModel):
    board_id: int | str = Field(..., description="The board's unique identifier.")
    item_id: int | str = Field(..., description="The item's unique identifier.")
    column_id: str = Field(..., description="The column's unique identifier.")
    timestamp: datetime = Field(..., description="The new date value")

class ChangeMultipleColumnQueryParams(BaseModel):
    board_id: int | str = Field(..., description="The board's unique identifier.")
    item_id: int | str = Field(..., description="The item's unique identifier.")
    column_values: Dict[str, Any] = Field(..., description="Column values in a json format")
    create_labels_if_missing: Optional[bool] = Field(default=False, description="Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)")

class MoveItemQueryParams(BaseModel):
    item_id: int = Field(..., description="The item's unique identifier.")
    group_id: str = Field(..., description="The group's unique identifier.")

class UploadFileQueryParams(BaseModel):
    item_id: int | str = Field(..., description="The item's unique identifier.")
    column_id: str = Field(..., description="The column's unique identifier.")
    file_path: str = Field(..., description="The path of the file on the user's system")
    mimetype: Optional[str] = Field(default=None, description="The mimetype of the file getting uploaded for example: application/json")

class UpdateQueryParams(BaseModel):
    item_id: int = Field(..., description="The item's unique identifier.")
    update_value: str = Field(..., description="Comments to be added to the item")

class FetchUpdateQueryParams(BaseModel):
    limit: int = Field(..., description="Number of items to get, the default is 25.")
    page: int = Field(..., description="Page number to get, starting at 1.")

class FetchUpdatesForItemsQueryParams(BaseModel):
    item_id: int = Field(..., description="The item's unique identifier.")
    limit: int = Field(..., description="Number of items to get, the default is 25.")

class FetchBoardUpdatesQueryParams(BaseModel):
    board_ids: int = Field(..., description="Board Id")
    updated_after: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")
    updated_before: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")

class FetchBoardUpdatestPageQueryParams(BaseModel):
    board_id: int | str = Field(..., description="Board Id")
    limit: int = Field(..., description="Number of items to get, the default is 25.")
    page: int = Field(..., description="Page number to get, starting at 1.")
    from_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")
    to_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")

class FetchActivityLogsFromBoardQueryParams(BaseModel):
    board_ids: int = Field(..., description="Board Id")
    page: int = Field(..., description="Page number to get, starting at 1.")
    limit: int = Field(..., description="Number of items to get, the default is 25.")
    from_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")
    to_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")

class FetchAllActivityLogsQueryParams(BaseModel):
    board_ids: int = Field(..., description="Board Id")
    from_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")
    to_date: str = Field(..., description="datetime in the format YYYY-MM-DDTHH:MM:SSZ")
    limit: int = Field(..., description="Number of items to get, the default is 25.")
    events_filter: List[str] = Field(..., description="Filter activity logs by specific event types")

class FetchItemsByColumnQueryParams(BaseModel):
    board_id: int | str = Field(..., description="Board Id")
    column_id: str = Field(..., description="column header")
    value: str = Field(..., description="Fetch column by this value")
    limit: Optional[int] = Field(default=None, description="Limit on number of rows to be fetched")
