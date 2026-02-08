from constants import MNT_DIR
from fastmcp import FastMCP
from fastmcp.server.providers import FileSystemProvider
from fastmcp.resources.types import DirectoryResource
from pathlib import Path

mcp = FastMCP(
    "My MCP Server",
    providers=[FileSystemProvider(Path(__file__).parent / "mcp", reload=True)],
)
mcp.add_resource(
    DirectoryResource(
        name="Files",
        uri="resource://files",  # type: ignore
        path=MNT_DIR,
        recursive=True,
        description="Lists all of the files on the file system",
    )
)

if __name__ == "__main__":
    mcp.run("http")
