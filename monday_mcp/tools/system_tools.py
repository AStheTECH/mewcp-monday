"""System group: monday_health_check"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from ..logging_utils import ToolLogger
from ..schemas.system import HealthCheckData, HealthCheckResult

logger = logging.getLogger("monday-mcp.tools.system")


def register_system_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="monday_health_check",
        description="Check server readiness and basic connectivity.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
    )
    def monday_health_check() -> HealthCheckResult:
        tlog = ToolLogger(logger, "monday_health_check")
        tlog.success()
        return HealthCheckResult(
            success=True,
            statusCode=200,
            data=HealthCheckData(
                status="ok",
                server="Monday.com MCP Server",
                type="third-party integration",
                auth_required="oauth token required",
            ),
        )
