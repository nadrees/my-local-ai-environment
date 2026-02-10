from pathlib import Path
from typing import Annotated

from fastmcp import Context
from fastmcp.dependencies import CurrentContext
from fastmcp.exceptions import ToolError
from fastmcp.tools.function_tool import tool
from pydantic import Field

from constants import MNT_DIR
from my_mcp.dataclasses.file import McpFile


@tool(
    description="""
    Writes the given contents to a file at the specified path. Returns the URI of the written file.
    """,
    annotations={
        "title": "Write File",
        "idempotentHint": True,
    },
)
async def write_file(
    file_path: Annotated[
        str,
        Field(
            description="""
            The full path to the file to write to, including file name and extension (if applicable).
            Even if the file has no extension, this tool will still create a FILE at the specified path, not a DIRECTORY.
            Any directories that are not yet created in the file path will be created automatically.
            If the file already exists, it will be overwritten.
            """,
            examples=[
                "/path/to/file.txt",
                "/path/to/directory/file",
            ],
        ),
    ],
    contents: Annotated[str, "The contents to write to the file."],
    ctx: Context = CurrentContext(),
) -> str:
    mcp_file = McpFile(file_path)

    try:
        p = mcp_file.resolve_path
    except ValueError as e:
        raise ToolError(str(e))

    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        f.write(contents)

    file_uri = str(mcp_file.as_uri())
    ctx.fastmcp.enable(keys={file_uri})
    return file_uri
