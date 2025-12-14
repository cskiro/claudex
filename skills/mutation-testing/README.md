# Mutation Testing

Evaluate test suite effectiveness by introducing deliberate code mutations and verifying tests catch them.

## Quick Start

```bash
# JavaScript/TypeScript (Stryker)
npm install --save-dev @stryker-mutator/core
npx stryker init
npx stryker run

# Python (mutmut)
pip install mutmut
mutmut run

# Java (PIT)
mvn org.pitest:pitest-maven:mutationCoverage
```

## What is Mutation Testing?

Mutation testing answers: **"Are my tests actually catching bugs?"**

1. Tool creates "mutants" (small code changes)
2. Runs your test suite against each mutant
3. Tests should fail (kill the mutant)
4. Surviving mutants = gaps in test coverage

## Mutation Score

```
Mutation Score = Killed Mutants / Total Mutants × 100
```

| Score | Quality |
|-------|---------|
| 90%+ | Excellent |
| 75-89% | Good |
| 50-74% | Fair |
| <50% | Needs work |

## When to Use

- Coverage is high but confidence is low
- Before major releases
- Validating critical code paths
- Finding tests that pass but don't catch real bugs

## When NOT to Use

- No existing test suite
- Coverage below 50%
- CI can't afford extra runtime (mutation testing is slow)

## Example Output

```
Mutant survived: src/utils/calculate.js:42
  Original: return total + tax
  Mutant:   return total - tax

  No test caught this mutation!
  Recommendation: Add test for tax calculation edge cases
```

## Performance Tips

- Target critical modules only (don't mutate everything)
- Use incremental mode in CI
- Run full mutation analysis weekly, incremental daily
- Parallelize across cores

## Resources

- [Stryker Mutator](https://stryker-mutator.io/)
- [PIT Mutation Testing](https://pitest.org/)
- [mutmut](https://mutmut.readthedocs.io/)
