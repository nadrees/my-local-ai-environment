import json

import pytest
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport
from mcp.types import TextResourceContents
from pydantic import AnyUrl

from mcp import ReadResourceResult
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


@pytest.mark.parametrize(
    "uri,expected_text",
    [
        (f"file://{test_file}", expected_text)
        for test_file, expected_text in TEST_FILES.items()
    ],
    ids=[test_file for test_file in TEST_FILES.keys()],
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
