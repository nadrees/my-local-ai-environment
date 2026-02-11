import pytest
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport
from mcp import ReadResourceResult
from mcp.types import CallToolResult, TextContent, TextResourceContents
from pydantic import AnyUrl

from my_mcp.dataclasses.file import McpFile
from tests.conftest import parse_files_from_resource_result


@pytest.mark.parametrize(
    "file_path,contents",
    [
        (
            "/test_file.txt",
            "This is a test file created by the write_file tool.",
        ),
        (
            "/test_dir/test_file.txt",
            "This is another test file created by the write_file tool.",
        ),
        (
            "/test_dir/sub_dir/test_file",
            "This is yet another test file created by the write_file tool.",
        ),
    ],
)
async def test_file_tool(
    mcp_client: Client[FastMCPTransport], file_path: str, contents: str
):
    result = await mcp_client.call_tool_mcp(
        "write_file",
        {
            "file_path": file_path,
            "contents": contents,
        },
    )

    expected_uri = f"file://{file_path}"
    result_content = result.content[0]
    assert isinstance(result_content, TextContent)
    assert result_content.text == expected_uri

    # Verify that the file was actually written to the file system
    read_result = await mcp_client.read_resource_mcp(expected_uri)
    assert read_result == ReadResourceResult(
        contents=[
            TextResourceContents(
                uri=AnyUrl(expected_uri),
                mimeType="text/plain",
                text=contents,
            )
        ]
    )


@pytest.mark.parametrize(
    "file_path",
    [
        "/invalid_path/\0/test_file.txt",
        "/test_dir/\0_invalid_file.txt",
        "/../test_file.txt",
        "/",
    ],
)
async def test_file_tool_invalid_path(
    mcp_client: Client[FastMCPTransport], file_path: str
):
    files = await mcp_client.read_resource("resource://files")
    files = parse_files_from_resource_result(files)

    invalid_file_path = file_path
    with pytest.raises(Exception):
        await mcp_client.call_tool(
            "write_file",
            {
                "file_path": invalid_file_path,
                "contents": "This should fail due to an invalid file path.",
            },
        )

    # Verify that the file was not created
    files_now = await mcp_client.read_resource("resource://files")
    files_now = parse_files_from_resource_result(files_now)
    assert files_now == files
