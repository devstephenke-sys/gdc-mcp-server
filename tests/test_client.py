"""Tests for GDC client."""

import pytest
from gdc_mcp.client import GDCClient


@pytest.mark.asyncio
async def test_client_initialization():
    """Test that client can be initialized."""
    client = GDCClient()
    assert client.token is None
    assert client._client is None


@pytest.mark.asyncio
async def test_client_with_token():
    """Test that client can be initialized with token."""
    client = GDCClient(token="test_token")
    assert client.token == "test_token"
    assert client._client is None
