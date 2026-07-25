"""Langfuse observability integration for the QuickVoice LiveKit voice agent."""

import os

from langfuse import Langfuse
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.util.types import AttributeValue

from livekit.agents.telemetry import set_tracer_provider

from utils.logger import logger


def setup_langfuse(metadata: dict[str, AttributeValue] | None = None) -> TracerProvider | None:
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST") or os.getenv("LANGFUSE_BASE_URL") or "https://cloud.langfuse.com"

    if not public_key or not secret_key:
        logger.warning("[langfuse] LANGFUSE_PUBLIC_KEY/SECRET_KEY not set; tracing disabled")
        return None

    trace_provider = TracerProvider()
    set_tracer_provider(trace_provider, metadata=metadata)

    Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        base_url=host,
        tracer_provider=trace_provider,
        should_export_span=lambda span: True,
    )

    logger.info("[langfuse] tracing enabled, exporting to {}", host)
    return trace_provider
