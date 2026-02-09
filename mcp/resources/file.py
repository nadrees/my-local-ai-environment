from pydantic import AnyUrl
from constants import MNT_DIR
from fastmcp.resources.function_resource import resource
from fastmcp.resources.resource import ResourceResult
from fastmcp.resources.types import FileResource
from fastmcp.exceptions import ResourceError
from mimetypes import guess_file_type


@resource("file://{path*}")
async def file(path: str) -> ResourceResult:
    """
    Reads the contents of the file on the file system at the given path and with the specified extension.
    """
    p = (MNT_DIR / path).absolute()
    # dont allow traversing out of the MNT_DIR
    if not p.is_relative_to(MNT_DIR):
        raise ResourceError(f"File {p.as_posix()} does not exist.")
    (mime_type, _) = guess_file_type(p)
    resource = FileResource(path=p, uri=AnyUrl(p.as_uri()))
    if mime_type is not None:
        resource.mime_type = mime_type
    return await resource.read()
