# Phase 2: Smart Clustering

**Purpose**: Group related insights using similarity analysis to identify skill candidates.

## Steps

### 1. Load clustering configuration
- Read `data/clustering-config.yaml` for weights and thresholds
- Similarity weights:
  - Same category: +0.3
  - Shared keyword: +0.1 per keyword
  - Temporal proximity (within 7 days): +0.05
  - Title similarity: +0.15
  - Content overlap: +0.2
- Clustering threshold: 0.6 minimum to group
- Standalone quality threshold: 0.8 for single-insight skills

### 2. Extract keywords from each insight
- Normalize text (lowercase, remove punctuation)
- Extract significant words from title (weight 2x)
- Extract significant words from body (weight 1x)
- Filter out common stop words
- Apply category-specific keyword boosting
- Build keyword vector for each insight

### 3. Calculate pairwise similarity scores
For each pair of insights (i, j):
- Base score = 0
- If same category: +0.3
- For each shared keyword: +0.1
- If dates within 7 days: +0.05
- Calculate title word overlap: shared_words / total_words * 0.15
- Calculate content concept overlap: shared_concepts / total_concepts * 0.2
- Final score = sum of all components

### 4. Build clusters
- Start with highest similarity pairs
- Group insights with similarity >= 0.6
- Use connected components algorithm
- Identify standalone insights (don't cluster with any others)
- For standalone insights, check if quality score >= 0.8

### 5. Assess cluster characteristics
For each cluster:
- Count insights
- Identify dominant category
- Extract common keywords
- Assess complexity (lines, code examples, etc.)
- Recommend skill complexity (minimal/standard/complex)
- Suggest skill pattern (phase-based/mode-based/validation)

### 6. Handle large clusters (>5 insights)
- Attempt sub-clustering by:
  - Temporal splits (early vs. late insights)
  - Sub-topic splits (different keyword groups)
  - Complexity splits (simple vs. complex insights)
- Ask user if they want to split or keep as comprehensive skill

### 7. Present clustering results interactively
For each cluster, show:
- Cluster ID and size
- Suggested skill name (from keywords)
- Dominant category
- Insight titles in cluster
- Similarity scores
- Recommended complexity

Ask user to:
- Review proposed clusters
- Accept/reject/modify groupings
- Combine or split clusters
- Remove low-value insights

## Output

Validated clusters of insights, each representing a skill candidate.

## Common Issues

- **All insights are unrelated** (no clusters): Offer to generate standalone skills or exit
- **One giant cluster**: Suggest sub-clustering or mode-based skill
- **Too many standalone insights**: Suggest raising similarity threshold or manual grouping
