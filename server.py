#!/usr/bin/env python3
"""MCP Server for Monday.com."""

import logging

from fastmcp import FastMCP
from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend
from starlette.responses import JSONResponse

from monday_mcp.cli import parse_args
from monday_mcp.config import BREAKING_CHANGES, SERVER_VERSION, configure_logging
from monday_mcp.tools import register_tools

configure_logging()
logger = logging.getLogger("monday-mcp")

backend = HeaderCredentialBackend()
mcp = FastMCP(
    "MewCP Monday.com MCP Server",
    version=SERVER_VERSION,
    middleware=[CredentialMiddleware(backend, "oauth")],
)
register_tools(mcp)


# /health MUST come before mcp.http_app() — routes are baked at http_app() time
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({
        "status": "healthy",
        "service": mcp.name,
        "version": SERVER_VERSION,
        "breaking_changes": BREAKING_CHANGES,
    })


# Expose ASGI app for hosting platform's (e.g. Vercel / Cloud Run) runtime.
app = mcp.http_app(path="/mcp", transport="streamable-http", stateless_http=True)


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("MewCP Monday.com MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
        logger.info(f"Transport: {args.transport}")
    if args.host:
        run_kwargs["host"] = args.host
        logger.info(f"Host: {args.host}")
    if args.port:
        run_kwargs["port"] = args.port
        logger.info(f"Port: {args.port}")

    try:
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise
