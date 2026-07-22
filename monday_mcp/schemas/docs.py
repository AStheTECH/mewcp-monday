"""Docs group schemas: get_document_with_blocks."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class CreatorData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None


class WorkspaceData(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str | None = None


class DocumentBlockData(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str | None = None
    content: str | None = None
    position: float | None = None
    updated_at: str | None = None
    id: str | None = None
    parent_block_id: str | None = None


class DocumentData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: CreatorData | None = None
    doc_folder_id: str | None = None
    doc_kind: str | None = None
    name: str | None = None
    url: str | None = None
    workspace: WorkspaceData | None = None
    workspace_id: str | None = None
    object_id: str | None = None
    settings: str | None = None
    blocks: list[DocumentBlockData] | None = None


class DocumentResult(ToolResult):
    data: DocumentData | None = None
