from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport
from mcp import ReadResourceResult
from mcp.types import CallToolResult, TextContent, TextResourceContents
from pydantic import AnyUrl


async def test_file_tool(mcp_client: Client[FastMCPTransport]):
    file_path = "/test_dir/test_file.txt"
    contents = "This is a test file created by the write_file tool."
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
