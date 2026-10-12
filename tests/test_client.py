"""Tests for GDC client."""

import pytest
from gdc_mcp.client import GDCClient


@pytest.mark.asyncio
async def test_client_initialization():
    """Test that client can be initialized."""
    client = GDCClient()
    assert client.token is None


@pytest.mark.asyncio
async def test_client_with_token():
    """Test that client can be initialized with token."""
    client = GDCClient(token="test_token")
    assert client.token == "test_token"


@pytest.mark.asyncio
async def test_client_context_manager():
    """Test that client works as context manager."""
    async with GDCClient() as client:
        assert client._client is not None
