# Maintenance

## Validation Contract

Use `./scripts/validate.sh` locally and in CI.

The default target is:

```bash
dotnet test F23.StringSimilarity.sln --configuration Release
```

## Dependency Notes

The library targets `netstandard2.0`; the test project targets `net6.0`. No lockfile or central package management file is currently present.

Before dependency maintenance, run:

```bash
dotnet list F23.StringSimilarity.sln package --outdated
```

## Release Notes

NuGet package metadata lives in `src/F23.StringSimilarity/F23.StringSimilarity.csproj`. Keep README examples, XML documentation, and tests aligned before publishing.
