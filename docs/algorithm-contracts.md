# Algorithm Contracts

Use this guide to choose an algorithm by the guarantees the library exposes.
It describes the current implementation; it does not change package or runtime
support policy.

## Choosing an algorithm

| Need | Use | Contract |
| --- | --- | --- |
| Exact edit count and metric-distance behavior | `Levenshtein` | Non-negative edit distance, zero only for equal input, symmetry, and triangle inequality. |
| Edit distance normalized to a 0–1 range | `NormalizedLevenshtein` | Distance and similarity are complementary (`similarity = 1 - distance`); the normalized result is not a metric. |
| Set overlap of character shingles | `Jaccard` | Similarity and distance are complementary values in the 0–1 range; the implementation is symmetric. Choose `k` to control shingle size. |

The README’s overview table remains the complete list of implemented
algorithms. Only use algorithms marked metric when callers rely on triangle
inequality (for example, metric indexing or pruning).

## Input and Unicode semantics

String overloads compare the .NET `string` representation directly: character
operations use UTF-16 code units. The library does not normalize Unicode,
perform culture-specific case folding, or segment grapheme clusters.

For example, the composed `"é"` and decomposed `"e\u0301"` representations are
not equal input and have a Levenshtein distance of two code-unit edits. Callers
who need canonical equivalence, culture-aware comparison, or user-perceived
character boundaries must normalize or segment input before calling an
algorithm.

## Null, empty, and large input behavior

- Public string APIs reject `null` with `ArgumentNullException`.
- Distance algorithms return zero for two empty inputs; normalized similarities
  return one for two equal inputs.
- Dynamic-programming algorithms such as `Levenshtein` have O(m*n) time cost.
  Keep very large comparison workloads bounded, batch them deliberately, and
  prefer the limit overload when callers only need to know whether a threshold
  was exceeded.

## Compatibility and validation

The library package targets `netstandard2.0`. The repository test project
targets `net6.0` and validates that consumer-facing surface with:

```bash
./scripts/validate.sh
```

Changing either target framework is a separate compatibility and release-policy
decision. It must not be inferred from this documentation or invariant suite.
