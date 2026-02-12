from pathlib import Path

from fastmcp import FastMCP
from fastmcp.resources.types import DirectoryResource
from fastmcp.server.providers import FileSystemProvider

from constants import MNT_DIR

mcp = FastMCP(
    "My MCP Server",
    providers=[FileSystemProvider(Path(__file__).parent / "my_mcp")],
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
    # Bind to 0.0.0.0 so the server is reachable from outside the container
    mcp.run("http", host="0.0.0.0", port=8000)
