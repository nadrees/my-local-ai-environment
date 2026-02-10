import json

import pytest
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport
from mcp import ReadResourceResult
from mcp.types import TextResourceContents
from pydantic import AnyUrl

from tests.conftest import TEST_FILES


async def test_files_resource(mcp_client: Client[FastMCPTransport]):
    result = await mcp_client.read_resource_mcp("resource://files")

    expected_text = {"files": [test_file for test_file in TEST_FILES.keys()]}
    expected_text = json.dumps(expected_text, indent=2, sort_keys=True)

    expected = ReadResourceResult(
        contents=[
            TextResourceContents(
                uri=AnyUrl("resource://files"),
                mimeType="application/json",
                text=expected_text,
            )
        ]
    )
    assert result == expected


ALL_TEST_FILES = []
for test_file, expected_text in TEST_FILES.items():
    # relative path
    ALL_TEST_FILES.append((f"file://{test_file}", expected_text))
    # absolute path
    ALL_TEST_FILES.append((f"file:///{test_file}", expected_text))


@pytest.mark.parametrize(
    "uri,expected_text",
    ALL_TEST_FILES,
    ids=[test_file for test_file, _ in ALL_TEST_FILES],
)
async def test_file_resource(
    mcp_client: Client[FastMCPTransport], uri: str, expected_text: str
):
    result = await mcp_client.read_resource_mcp(uri)
    expected = ReadResourceResult(
        contents=[
            TextResourceContents(
                uri=AnyUrl(uri),
                mimeType="text/plain",
                text=expected_text,
            )
        ]
    )
    assert result == expected


@pytest.mark.parametrize(
    "uri",
    [
        "file://nonexistent_file.txt",
        "file://sub_dir/nonexistent_file.txt",
        "file://",
        "file://../",
    ],
)
async def test_nonexistent_file_resource(
    mcp_client: Client[FastMCPTransport], uri: str
):
    with pytest.raises(Exception) as exc_info:
        await mcp_client.read_resource_mcp(uri)
    assert "No such file or directory" in str(
        exc_info.value
    ) or "Attempt to navigate higher than root" in str(exc_info.value)
