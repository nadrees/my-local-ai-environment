from mimetypes import guess_file_type

from fastmcp.exceptions import ResourceError
from fastmcp.resources.function_resource import resource
from fastmcp.resources.resource import ResourceResult
from fastmcp.resources.types import FileResource

from my_mcp.dataclasses.file import McpFile


@resource("file://{path*}")
async def file(path: str) -> ResourceResult:
    """
    Reads the contents of the file on the file system at the given path and with the specified extension.
    """
    f = McpFile(path)
    try:
        p = f.resolve_path
    except ValueError as e:
        raise ResourceError(str(e))

    if not p.exists():
        raise ResourceError(f"No such file or directory: '{path}'")

    (mime_type, _) = guess_file_type(p)
    resource = FileResource(path=p, uri=f.as_uri())
    if mime_type is not None:
        resource.mime_type = mime_type
    return await resource.read()
