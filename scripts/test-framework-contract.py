#!/usr/bin/env python3
"""Fail closed when the documented framework compatibility contract drifts."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LIBRARY_PROJECT = ROOT / "src/F23.StringSimilarity/F23.StringSimilarity.csproj"
TEST_PROJECT = ROOT / "test/F23.StringSimilarity.Tests/F23.StringSimilarity.Tests.csproj"


def evaluated_target(path: Path, configuration: str | None = None) -> str:
    selected_configuration = configuration or os.environ.get(
        "CONFIGURATION",
        "Release",
    )
    with tempfile.TemporaryDirectory(prefix="string-similarity-framework-") as temp:
        targets = Path(temp) / "report-framework.targets"
        targets.write_text(
            """<Project>
  <Target Name="ReportFrameworkContract">
    <Message Text="FRAMEWORK_CONTRACT=$(TargetFramework)" Importance="high" />
  </Target>
</Project>
""",
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                "dotnet",
                "msbuild",
                str(path),
                "-nologo",
                "-target:ReportFrameworkContract",
                f"-property:CustomAfterMicrosoftCommonTargets={targets}",
                f"-property:Configuration={selected_configuration}",
                "-verbosity:minimal",
            ],
            cwd=path.parent,
            text=True,
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        raise AssertionError(
            f"MSBuild evaluation failed for {path}: {result.stderr.strip()}"
        )
    values = [
        line.split("FRAMEWORK_CONTRACT=", 1)[1].strip()
        for line in result.stdout.splitlines()
        if "FRAMEWORK_CONTRACT=" in line
    ]
    if len(values) != 1 or not values[0]:
        raise AssertionError(
            f"MSBuild did not report exactly one TargetFramework for {path}"
        )
    return values[0]


def require_target(
    path: Path,
    expected: str,
    label: str | None = None,
    configuration: str | None = None,
) -> None:
    actual = evaluated_target(path, configuration)
    if actual != expected:
        name = label or str(path.relative_to(ROOT))
        raise AssertionError(f"{name} targets {actual}; expected {expected}")


def require_repository_target(
    path: Path,
    expected: str,
    label: str | None = None,
    configuration: str | None = None,
) -> None:
    selected = configuration or os.environ.get("CONFIGURATION", "Release")
    require_target(path, expected, label, configuration="Release")
    if selected != "Release":
        require_target(path, expected, label, configuration=selected)


def require_evaluation_regressions() -> None:
    with tempfile.TemporaryDirectory(prefix="string-similarity-fixtures-") as temp:
        fixture_root = Path(temp)
        indirect = fixture_root / "indirect.csproj"
        indirect.write_text(
            """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <ContractTarget>netstandard2.0</ContractTarget>
    <TargetFramework>$(ContractTarget)</TargetFramework>
  </PropertyGroup>
</Project>
""",
            encoding="utf-8",
        )
        require_target(indirect, "netstandard2.0", "property-indirected fixture")

        conditional = fixture_root / "conditional.csproj"
        conditional.write_text(
            """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup Condition="'$(Configuration)' == 'Debug'">
    <TargetFramework>net6.0</TargetFramework>
  </PropertyGroup>
</Project>
""",
            encoding="utf-8",
        )
        require_target(
            conditional,
            "net6.0",
            "non-default conditional fixture",
            configuration="Debug",
        )

        release_drift = fixture_root / "release-drift.csproj"
        release_drift.write_text(
            """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)' == 'Debug'">
    <TargetFramework>net6.0</TargetFramework>
  </PropertyGroup>
</Project>
""",
            encoding="utf-8",
        )
        try:
            require_repository_target(
                release_drift,
                "net6.0",
                "release drift fixture",
                configuration="Debug",
            )
        except AssertionError:
            pass
        else:
            raise AssertionError("non-default configuration hid Release drift")

        imported = fixture_root / "imported.csproj"
        imported.write_text(
            """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
  </PropertyGroup>
  <Import Project="override.props" />
</Project>
""",
            encoding="utf-8",
        )
        (fixture_root / "override.props").write_text(
            """<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
</Project>
""",
            encoding="utf-8",
        )
        try:
            require_target(imported, "netstandard2.0", "imported override fixture")
        except AssertionError:
            pass
        else:
            raise AssertionError("imported target override fixture was accepted")


def main() -> int:
    require_repository_target(LIBRARY_PROJECT, "netstandard2.0")
    require_repository_target(TEST_PROJECT, "net6.0")
    require_evaluation_regressions()
    print("framework compatibility contract passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"framework compatibility contract failed: {error}", file=sys.stderr)
        raise SystemExit(1)
