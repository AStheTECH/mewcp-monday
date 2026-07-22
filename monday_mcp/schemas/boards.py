"""Boards group schemas: fetch_boards, fetch_boards_by_id, fetch_all_items_by_board_id,
fetch_item_by_board_id_by_update_date, fetch_columns_by_board_id."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


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


class GroupData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None


class ColumnData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None
    type: str | None = None


class BoardData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    updated_at: str | None = None
    groups: list[GroupData] | None = None
    columns: list[ColumnData] | None = None


class BoardListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    boards: list[BoardData]


class BoardListResult(ToolResult):
    data: BoardListData | None = None


class BoardResult(ToolResult):
    data: BoardData | None = None


class ColumnValueData(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str | None = None
    text: str | None = None
    type: str | None = None
    column: ColumnData | None = None
    display_value: str | None = None


class ItemData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    state: str | None = None
    name: str | None = None
    updated_at: str | None = None
    group: GroupData | None = None
    subitems: Optional[list["ItemData"]] = None
    parent_item: Optional["ItemData"] = None
    column_values: list[ColumnValueData] | None = None


ItemData.model_rebuild()


class ItemListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[ItemData]


class ItemListResult(ToolResult):
    data: ItemListData | None = None
