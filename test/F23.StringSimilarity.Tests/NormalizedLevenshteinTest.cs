/*
 * The MIT License
 *
 * Copyright 2017 feature[23]
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

using System;
using System.Diagnostics.CodeAnalysis;
using F23.StringSimilarity.Tests.TestUtil;
using Xunit;

namespace F23.StringSimilarity.Tests
{
    [SuppressMessage("ReSharper", "ArgumentsStyleLiteral")]
    [SuppressMessage("ReSharper", "ArgumentsStyleNamedExpression")]
    [SuppressMessage("ReSharper", "ArgumentsStyleOther")]
    public class NormalizedLevenshteinTest
    {
        [InlineData("My string", "My tring", 0.111111)]
        [InlineData("My string", "M string2", 0.222222)]
        [InlineData("kitten", "sitting", 0.428571)]
        [Theory]
        public void TestDistance(string s1, string s2, double expected)
        {
            var instance = new NormalizedLevenshtein();

            Assert.Equal(expected, actual: instance.Distance(s1, s2), precision: 6);
            Assert.Equal(expected, actual: instance.Distance(s1.AsSpan(), s2.AsSpan()), precision: 6);
            Assert.Equal(
                expected,
                actual: instance.Distance<byte>(
                    System.Text.Encoding.Latin1.GetBytes(s1).AsSpan(),
                    System.Text.Encoding.Latin1.GetBytes(s2).AsSpan()),
                precision: 6);
        }

        [InlineData("My string", "My tring", 0.888889)]
        [InlineData("My string", "M string2", 0.777778)]
        [InlineData("kitten", "sitting", 0.571429)]
        [Theory]
        public void TestSimilarity(string s1, string s2, double expected)
        {
            var instance = new NormalizedLevenshtein();

            Assert.Equal(expected, actual: instance.Similarity(s1, s2), precision: 6);
            Assert.Equal(expected, actual: instance.Similarity(s1.AsSpan(), s2.AsSpan()), precision: 6);
            Assert.Equal(
                expected,
                actual: instance.Similarity<byte>(
                    System.Text.Encoding.Latin1.GetBytes(s1).AsSpan(),
                    System.Text.Encoding.Latin1.GetBytes(s2).AsSpan()),
                precision: 6);
        }

        [Fact]
        public void NullEmptyDistanceTest()
        {
            var instance = new NormalizedLevenshtein();
            NullEmptyTests.TestDistance(instance);
        }

        [Fact]
        public void NullEmptySimilarityTest()
        {
            var instance = new NormalizedLevenshtein();
            NullEmptyTests.TestSimilarity(instance);
        }
    }
}
