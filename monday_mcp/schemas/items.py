"""Items group schemas: create_item, create_subitem, change_simple_column_value,
change_status_column_value, change_date_column_value, change_custom_column_value,
change_multiple_column_values, move_item_to_group, archive_item_by_id,
delete_item_by_id, upload_file_to_column, fetch_items_by_column_value,
fetch_items_by_id."""

from typing import Optional

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class CreatedItemData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None


class CreatedItemResult(ToolResult):
    data: CreatedItemData | None = None


class SubitemColumnValueData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    text: str | None = None


class SubitemBoardData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None


class SubitemData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    column_values: list[SubitemColumnValueData] | None = None
    board: SubitemBoardData | None = None


class SubitemResult(ToolResult):
    data: SubitemData | None = None


class ItemIdData(BaseModel):
    """Shared shape for mutations that return only {"id": ...}:
    change_simple_column_value, move_item_to_group, archive_item_by_id, delete_item_by_id."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ItemIdResult(ToolResult):
    data: ItemIdData | None = None


class ColumnChangeColumnValueData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    text: str | None = None
    value: str | None = None


class ColumnChangeData(BaseModel):
    """Shared shape for the change_column_value mutation, reached via
    change_status_column_value, change_date_column_value, change_custom_column_value."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    column_values: list[ColumnChangeColumnValueData] | None = None


class ColumnChangeResult(ToolResult):
    data: ColumnChangeData | None = None


class ColumnValuesChangeColumnValueData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    text: str | None = None


class ColumnValuesChangeData(BaseModel):
    """change_multiple_column_values has no "value" field on its column_values entries,
    unlike ColumnChangeData — kept separate per the no-sharing-unless-identical rule."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    column_values: list[ColumnValuesChangeColumnValueData] | None = None


class ColumnValuesChangeResult(ToolResult):
    data: ColumnValuesChangeData | None = None


class FileUploadData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    url: str | None = None
    file_extension: str | None = None
    file_size: int | None = None


class FileUploadResult(ToolResult):
    data: FileUploadData | None = None


class GroupData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None


class ColumnData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    title: str | None = None
    type: str | None = None


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


class ItemPageData(BaseModel):
    model_config = ConfigDict(extra="allow")

    cursor: str | None = None
    items: list[ItemData]


class ItemPageResult(ToolResult):
    data: ItemPageData | None = None
