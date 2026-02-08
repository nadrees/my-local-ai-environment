from pydantic import AnyUrl
from constants import MNT_DIR
from fastmcp.resources.function_resource import resource
from fastmcp.resources.resource import ResourceResult
from fastmcp.resources.types import FileResource
from mimetypes import guess_file_type


@resource("file://{path*}.{extension}/")
async def file(path: str, extension: str) -> ResourceResult:
    """
    Reads the contents of the file on the file system at the given path and with the specified extension.
    """
    p = (MNT_DIR / path).with_suffix("." + extension).absolute()
    (mime_type, _) = guess_file_type(p)
    resource = FileResource(path=p, uri=AnyUrl(p.as_uri()))
    if mime_type is not None:
        resource.mime_type = mime_type
    return await resource.read()
