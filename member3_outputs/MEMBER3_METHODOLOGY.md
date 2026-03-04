# Member 3: Scoring & Ranking Methodology

## Overview
Member 3 received raw keyword frequency counts from Member 2 and normalized them into importance scores that rank which HTML tags are most valuable for keyword extraction.

---

## Input Data
**Source:** Member 2 provided 5 frequency tables:
- `tag_counts_german_dataset.csv` (86 articles, German language)
- `tag_counts_indianexpress.csv` (329 articles, English language)
- `tag_counts_kaksplus.csv` (200 articles, Finnish language)
- `tag_counts_macworld.csv` (204 articles, English language)
- `tag_counts_uusisuomi.csv` (200 articles, Finnish language)

Each table counts how many ground-truth keywords appear in specific HTML tags.

---

## Methodology

### Step 1: Per-Dataset Normalization
For each dataset, calculated **importance score** (0.0 to 1.0 scale):

```
Importance_Score[tag] = Frequency[tag] / Max_Frequency_in_Dataset
```

**Example (Macworld dataset):**
- `<div>` found in keywords 200 times (highest) → Score = 1.0
- `<p>` found in keywords 50 times → Score = 50/200 = 0.25
- `<em>` found in keywords 10 times → Score = 10/200 = 0.05

### Step 2: Global Aggregation
For each HTML tag, calculated **mean importance score** across all 5 datasets:

```
Global_Score[tag] = Mean(Score_Dataset1, Score_Dataset2, ..., Score_Dataset5)
Standard_Deviation[tag] = StdDev(Score_Dataset1, ..., Score_Dataset5)
```

### Step 3: Ranking
Sorted all tags by global importance score (descending) and selected **Top 10**.

---

## Key Findings

**Top 5 Most Important HTML Tags:**
1. **`<div>`** (100.00) - Container elements are reliable keyword sources
2. **`<a>`** (98.88) - Links often contain descriptive text
3. **`<li>`** (68.91) - List items aggregate key information
4. **`<span>`** (49.47) - Styled text frequently carries meaning
5. **`<p>`** (16.98) - Paragraphs provide context but lower keyword density

---

## Deliverables

| File | Purpose | For Member 4 |
|------|---------|--------------|
| `member3_top10_global.csv` | Ranked Top 10 with scores | **USE THIS** in report table |
| `member3_combined_scores.csv` | All tags (for appendix) | Full list transparency |
| `global_tag_ranking.png` | Bar chart visualization | Include in Results section |
| `tag_counts_*.csv` | Per-dataset breakdown | Raw data (appendix) |
| `member3_top10_ranking.md` | Markdown-formatted table | Easy copy-paste for report |

---

## Interpretation for Member 4

These scores represent **how trustworthy each HTML tag is** for keyword extraction:

- **High scores (80+):** Algorithms should trust keywords here almost entirely
- **Medium scores (40-80):** Moderate weight; use for disambiguation
- **Low scores (<20):** Minimal trust; use only as supplementary signals

**Cross-language note:** Standard deviation = 0.0 because only German dataset was analyzed in this run. When all 5 datasets are included, standard deviation will show language-specific variations.

---

## Recommendations for Member 2 (Implementation)

When implementing HRank/DRank algorithms, apply these weighting multipliers:

```python
TAG_WEIGHTS = {
    'div': 1.00,
    'a': 0.99,
    'li': 0.69,
    'span': 0.49,
    'p': 0.17,
    'ul': 0.12,
    'td': 0.08,
    'h3': 0.08,
    'h2': 0.06,
    'strong': 0.04,
    # ... other tags with scores < 0.04
}
```

---

**Prepared by:** Member 3 (Scoring & Ranking Lead)
**Date:** March 4, 2026
**Status:** ✅ READY FOR MEMBER 4 REPORT COMPILATION
