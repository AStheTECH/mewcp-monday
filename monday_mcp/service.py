import logging

from fastmcp_credentials import get_credentials
from monday_sdk import MondayClient

logger = logging.getLogger("monday-mcp-server")


def get_client():
    cred = get_credentials()
    client = MondayClient(token=cred.access_token)
    logger.info("Google monday service created successfully")
    return client
