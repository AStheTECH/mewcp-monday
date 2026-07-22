"""Upstream API client for MewCP Monday MCP Server."""

import logging

from fastmcp_credentials import get_credentials
from monday_sdk import MondayClient

logger = logging.getLogger("monday-mcp.service")


def get_client():
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    client = MondayClient(token=cred.access_token)
    logger.info("Monday.com service created successfully")
    return client
