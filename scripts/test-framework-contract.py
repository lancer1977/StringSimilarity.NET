#!/usr/bin/env python3
"""Fail closed when the documented framework compatibility contract drifts."""

from __future__ import annotations

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
LIBRARY_PROJECT = ROOT / "src/F23.StringSimilarity/F23.StringSimilarity.csproj"
TEST_PROJECT = ROOT / "test/F23.StringSimilarity.Tests/F23.StringSimilarity.Tests.csproj"


def target_framework(project_xml: str) -> str:
    root = ET.fromstring(project_xml)
    values = [
        element.text.strip()
        for element in root.iter("TargetFramework")
        if element.text and element.text.strip()
    ]
    if len(values) != 1:
        raise AssertionError(
            f"project must declare exactly one TargetFramework, found {len(values)}"
        )
    return values[0]


def require_target_xml(project_xml: str, expected: str, label: str) -> None:
    actual = target_framework(project_xml)
    if actual != expected:
        raise AssertionError(f"{label} targets {actual}; expected {expected}")


def require_target(path: Path, expected: str) -> None:
    require_target_xml(
        path.read_text(encoding="utf-8-sig"),
        expected,
        str(path.relative_to(ROOT)),
    )


def require_negative_fixtures() -> None:
    fixtures = (
        ("<Project><TargetFramework>net8.0</TargetFramework></Project>", "netstandard2.0"),
        ("<Project><TargetFramework>net8.0</TargetFramework></Project>", "net6.0"),
        ("<Project />", "netstandard2.0"),
        (
            "<Project><TargetFramework>net6.0</TargetFramework>"
            "<TargetFramework>net8.0</TargetFramework></Project>",
            "net6.0",
        ),
    )
    for project_xml, expected in fixtures:
        try:
            require_target_xml(project_xml, expected, "negative fixture")
        except (AssertionError, ET.ParseError):
            continue
        raise AssertionError(f"framework drift fixture was accepted: {expected}")


def main() -> int:
    require_target(LIBRARY_PROJECT, "netstandard2.0")
    require_target(TEST_PROJECT, "net6.0")
    require_negative_fixtures()
    print("framework compatibility contract passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, ET.ParseError) as error:
        print(f"framework compatibility contract failed: {error}", file=sys.stderr)
        raise SystemExit(1)
