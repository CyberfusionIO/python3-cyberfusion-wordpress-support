"""Comparable version type."""

from functools import total_ordering
from typing import Tuple


@total_ordering
class Version:
    """Comparable representation of a dot-separated version string.

    Only the leading integer of each dot-separated part is kept, so a suffix
    such as '7.1.0-beta.1' still parses. Parts are compared numerically, with
    missing trailing parts treated as zero (so '7.1' equals '7.1.0').
    """

    def __init__(self, version: str) -> None:
        """Set attributes."""
        self.version = version

        self.parts = self._parse(version)

    @staticmethod
    def _parse(version: str) -> Tuple[int, ...]:
        """Parse a version string into a tuple of ints."""
        parts = []

        for part in version.split("."):
            digits = ""

            for character in part:
                if not character.isdigit():
                    break

                digits += character

            parts.append(int(digits) if digits else 0)

        return tuple(parts)

    def _padded(self, other: "Version") -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        """Pad both part tuples to equal length with trailing zeroes."""
        length = max(len(self.parts), len(other.parts))

        return (
            self.parts + (0,) * (length - len(self.parts)),
            other.parts + (0,) * (length - len(other.parts)),
        )

    def __eq__(self, other: object) -> bool:
        """Compare for equality."""
        if not isinstance(other, Version):
            return NotImplemented

        own, theirs = self._padded(other)

        return own == theirs

    def __lt__(self, other: object) -> bool:
        """Compare for ordering."""
        if not isinstance(other, Version):
            return NotImplemented

        own, theirs = self._padded(other)

        return own < theirs

    def __hash__(self) -> int:
        """Hash by parsed parts.

        Trailing zeroes are stripped so equal versions (e.g. '7.1' and '7.1.0')
        hash the same.
        """
        parts = self.parts

        while parts and parts[-1] == 0:
            parts = parts[:-1]

        return hash(parts)

    def __repr__(self) -> str:
        """Get representation."""
        return f"Version({self.version!r})"
