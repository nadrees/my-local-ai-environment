import importlib

import pytest
from fastmcp.client import Client

import constants

TEST_FILES = {
    "test_file.txt": "This is a test file.",
    "sub_dir/test_file_2.txt": "This is a second test file.",
}


@pytest.fixture
async def file_system(tmp_path):
    for relative_path, contents in TEST_FILES.items():
        file_path = tmp_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(contents)
    yield tmp_path


@pytest.fixture
async def mcp_client(file_system, monkeypatch):
    monkeypatch.setattr(constants, "MNT_DIR", file_system)
    import main

    importlib.reload(main)
    async with Client(transport=main.mcp) as client:
        yield client
