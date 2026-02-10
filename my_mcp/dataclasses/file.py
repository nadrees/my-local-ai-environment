from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from pydantic import AnyUrl

from constants import MNT_DIR


@dataclass
class McpFile:
    path: str

    @cached_property
    def resolve_path(self) -> Path:
        """
        Resolves the path to the absolute path relative to MNT_DIR and prevents directory traversal attacks.
        """
        if self.path.startswith("/"):
            # Remove leading slash to prevent absolute path issues
            self.path = self.path[1:]
        p = (MNT_DIR / self.path).resolve()
        if not p.is_relative_to(MNT_DIR):
            raise ValueError(
                f"Attempt to navigate higher than root directory: {self.path}."
            )
        return p

    def as_uri(self) -> AnyUrl:
        """
        Returns the file URI for this file.
        """
        p = "/" / self.resolve_path.relative_to(MNT_DIR)
        return AnyUrl(p.as_uri())

    def exists(self) -> bool:
        """
        Checks if the file exists.
        """
        p = self.resolve_path
        return p.exists()
