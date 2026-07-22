"""Docs group: get_document_with_blocks."""

import dataclasses
import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.docs import DocumentData, DocumentResult
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("monday-mcp.tools.docs")


def register_docs_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_document_with_blocks",
        description="Fetch a document with all blocks (auto-paginates).",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_document_with_blocks(
        doc_id: str = Field(..., description="doc id"),
    ) -> DocumentResult:
        tlog = ToolLogger(logger, "get_document_with_blocks")
        try:
            document = service.get_client().docs.get_document_with_blocks(doc_id=doc_id)
            if document is None:
                return _err(DocumentResult, tlog, "NOT_FOUND", f"Document {doc_id} not found", 404)
            tlog.success()
            return DocumentResult(
                success=True, statusCode=200,
                data=DocumentData(**dataclasses.asdict(document)),
            )
        except Exception as exc:
            return _handle_request_exc(DocumentResult, tlog, exc)
