# Scripts

## Validate

Run the repo's validation target:

```bash
./scripts/validate.sh
```

The script first verifies the `netstandard2.0` library / `net6.0` test
compatibility contract, then defaults to `F23.StringSimilarity.sln` with
`CONFIGURATION=Release`. Override `VALIDATION_TARGET` or pass extra
`dotnet test` arguments when needed.
