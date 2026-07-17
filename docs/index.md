# StringSimilarity.NET

`StringSimilarity.NET` is a .NET string similarity and distance library.

## Repository Layout

- `src/F23.StringSimilarity/` contains the library source.
- `test/F23.StringSimilarity.Tests/` contains xUnit coverage.
- `build/CreateNugetPackage.ps1` contains legacy package creation helpers.
- `scripts/validate.sh` is the local validation entry point.

## Consumer contracts

- [Algorithm contracts](algorithm-contracts.md) documents selection guidance,
  metric/normalization guarantees, UTF-16 Unicode semantics, null/empty
  behavior, large-input limits, and the current target-framework matrix.

## Validation

```bash
./scripts/validate.sh
```

The validator runs the solution tests in `Release` configuration unless overridden.
