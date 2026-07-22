"""Updates group schemas: create_update, delete_update, fetch_updates,
fetch_updates_for_item, fetch_board_updates, fetch_board_updates_page."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class UpdateIdData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None


class UpdateIdResult(ToolResult):
    data: UpdateIdData | None = None


class SimpleUpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    body: str | None = None


class SimpleUpdateListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    updates: list[SimpleUpdateData]


class SimpleUpdateListResult(ToolResult):
    data: SimpleUpdateListData | None = None


class ItemCreatorData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    email: str | None = None


class UpdateAssetData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    url: str | None = None
    file_extension: str | None = None
    file_size: str | None = None


class UpdateReplyData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    body: str | None = None
    creator: ItemCreatorData | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ItemUpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    body: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    creator: ItemCreatorData | None = None
    assets: list[UpdateAssetData] | None = None
    replies: list[UpdateReplyData] | None = None


class ItemUpdateListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    updates: list[ItemUpdateData]


class ItemUpdateListResult(ToolResult):
    data: ItemUpdateListData | None = None


class CreatorData(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None
    id: str | None = None


class UpdateData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    text_body: str | None = None
    item_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    creator: CreatorData | None = None


class UpdateListData(BaseModel):
    model_config = ConfigDict(extra="allow")

    updates: list[UpdateData]


class UpdateListResult(ToolResult):
    data: UpdateListData | None = None
