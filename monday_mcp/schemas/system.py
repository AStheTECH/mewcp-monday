"""System group schemas: monday_health_check."""

from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class HealthCheckData(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str
    server: str
    type: str
    auth_required: str


class HealthCheckResult(ToolResult):
    data: HealthCheckData | None = None
