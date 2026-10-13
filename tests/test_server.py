"""Tests for GDC MCP server."""

import pytest
from gdc_mcp.server import mcp


def test_server_initialization():
    """Test that MCP server can be initialized."""
    assert mcp is not None
    assert hasattr(mcp, "_tool_manager")


def test_tools_registered():
    """Test that tools are registered with the server."""
    tool_manager = mcp._tool_manager
    tools = tool_manager.list_tools()
    
    # Check that expected tools are registered
    tool_names = {tool.name for tool in tools}
    
    expected_tools = {
        "get_status",
        "search_projects",
        "get_project_details",
        "search_cases",
        "get_case_details",
        "search_files",
        "get_file_details",
        "search_annotations",
        "query_mutations",
        "query_copy_number",
        "query_expression",
        "query_methylation",
        "get_manifest",
        "get_mapping",
    }
    
    assert expected_tools.issubset(tool_names), f"Missing tools: {expected_tools - tool_names}"
