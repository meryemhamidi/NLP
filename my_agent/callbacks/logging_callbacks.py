"""Callback utilities for observability (agents, models, tools)."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.adk.models.llm_response import LlmResponse
from google.adk.models.llm_request import LlmRequest

logger = logging.getLogger("event_planner.callbacks")


def agent_start_logger(callback_context: CallbackContext) -> None:
    """Logs the start of an agent execution."""
    logger.info(
        "Agent start",
        extra={
            "agent": callback_context.agent_name,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


def agent_end_logger(callback_context: CallbackContext) -> None:
    """Logs the end of an agent execution."""
    logger.info(
        "Agent end",
        extra={
            "agent": callback_context.agent_name,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


def before_model_logger(
    callback_context: CallbackContext, llm_request: LlmRequest, **_: Any
) -> Optional[LlmResponse]:
    """Logs outgoing model request metadata."""
    logger.info(
        "Model request",
        extra={
            "agent": callback_context.agent_name,
            "model": llm_request.model,
            "tokens_estimate": len(str(llm_request.contents or "")) // 4,
        },
    )
    return None


# Aliases to fit ADK callback naming used in agents.
before_agent_logger = agent_start_logger
after_agent_logger = agent_end_logger


def after_model_logger(
    callback_context: CallbackContext, llm_response: LlmResponse, **_: Any
) -> Optional[LlmResponse]:
    """Logs token usage and latency after the model responds."""
    usage = getattr(llm_response, "usage", None)
    logger.info(
        "Model response",
        extra={
            "agent": callback_context.agent_name,
            "input_tokens": getattr(usage, "input_tokens", None) if usage else None,
            "output_tokens": getattr(usage, "output_tokens", None) if usage else None,
        },
    )
    return None


def before_tool_logger(
    tool: BaseTool,
    tool_input: dict[str, Any] | None = None,
    ctx: ToolContext | None = None,
    *args: Any,
    **_: Any,
) -> Optional[dict[str, Any]]:
    """Logs tool calls with parameters."""
    logger.info(
        "Tool call",
        extra={
            "tool": tool.name,
            "params": tool_input,
            "agent": getattr(ctx, "agent_name", None),
        },
    )
    return None


def after_tool_logger(
    tool: BaseTool,
    tool_input: dict[str, Any] | None = None,
    ctx: ToolContext | None = None,
    tool_output: dict | Any | None = None,
    *args: Any,
    **_: Any,
) -> Optional[dict[str, Any]]:
    """Logs tool results (truncated)."""
    preview = json.dumps(tool_output, default=str)[:500] if tool_output is not None else None
    logger.info(
        "Tool result",
        extra={
            "tool": tool.name,
            "agent": getattr(ctx, "agent_name", None),
            "result_preview": preview,
        },
    )
    return None
