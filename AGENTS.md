# Agent Notes

## Purpose

`StringSimilarity.NET` is a .NET port of `java-string-similarity`. It provides string distance and similarity algorithms such as Levenshtein, Jaro-Winkler, N-Gram, Cosine, Jaccard, Sorensen-Dice, and Ratcliff-Obershelp.

## Validation

Run the repository validation script before handoff:

```bash
./scripts/validate.sh
```

The script runs `dotnet test F23.StringSimilarity.sln --configuration Release`.

## Stewardship

- Preserve algorithm behavior with focused tests in `test/F23.StringSimilarity.Tests`.
- Keep README examples and the algorithm summary table aligned with implemented classes.
- Package publishing is handled separately from validation; do not add release credentials to CI.
