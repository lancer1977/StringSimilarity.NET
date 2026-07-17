using System;
using Xunit;

namespace F23.StringSimilarity.Tests
{
    public class ContractInvariantTests
    {
        private static readonly string[] Samples =
        {
            string.Empty,
            "a",
            "ab",
            "kitten",
            "sitting",
            "é",
            "e\u0301",
            "🇺🇸",
        };

        [Fact]
        public void LevenshteinIsSymmetricAndSatisfiesTriangleInequalityForRepresentativeInputs()
        {
            var distance = new Levenshtein();

            foreach (var left in Samples)
            {
                Assert.Equal(0.0, distance.Distance(left, left));
                foreach (var right in Samples)
                {
                    Assert.Equal(distance.Distance(left, right), distance.Distance(right, left));
                    foreach (var pivot in Samples)
                    {
                        Assert.True(
                            distance.Distance(left, right) <= distance.Distance(left, pivot) + distance.Distance(pivot, right),
                            $"Triangle inequality failed for '{left}', '{pivot}', and '{right}'.");
                    }
                }
            }
        }

        [Fact]
        public void NormalizedLevenshteinStaysBoundedSymmetricAndComplementary()
        {
            var distance = new NormalizedLevenshtein();

            foreach (var left in Samples)
            {
                foreach (var right in Samples)
                {
                    var value = distance.Distance(left, right);
                    Assert.InRange(value, 0.0, 1.0);
                    Assert.Equal(value, distance.Distance(right, left), 12);
                    Assert.Equal(1.0, value + distance.Similarity(left, right), 12);
                }
            }
        }

        [Fact]
        public void JaccardIsBoundedSymmetricAndComplementary()
        {
            var similarity = new Jaccard(k: 1);

            foreach (var left in Samples)
            {
                foreach (var right in Samples)
                {
                    var value = similarity.Similarity(left, right);
                    Assert.InRange(value, 0.0, 1.0);
                    Assert.Equal(value, similarity.Similarity(right, left), 12);
                    Assert.Equal(1.0, value + similarity.Distance(left, right), 12);
                }
            }
        }

        [Fact]
        public void AlgorithmsOperateOnUtf16CodeUnitsWithoutImplicitNormalization()
        {
            var distance = new Levenshtein();

            Assert.Equal(2.0, distance.Distance("é", "e\u0301"));
            Assert.Equal(4.0, distance.Distance("🇺🇸", "US"));
        }

        [Fact]
        public void LevenshteinHandlesALargeNearMatchWithoutChangingTheResultContract()
        {
            var distance = new Levenshtein();
            var source = new string('a', 2048);
            var candidate = source[..2047] + "b";

            Assert.Equal(1.0, distance.Distance(source, candidate));
        }
    }
}
