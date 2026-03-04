# Member 3: Scoring & Ranking – Final Deliverables

## Executive Summary
This document contains the final scoring, normalization, and Top-10 ranking of HTML tags by keyword importance across all analyzed datasets (Macworld, IndianExpress, Kaksplus, Uusisuomi, German).

---

## Scoring Methodology

### Importance Score Formula
$$\text{Importance Score}(tag) = \frac{\text{Keyword Occurrences}(tag)}{\text{Max Occurrences}} \times 100\%$$

Where:
- **Keyword Occurrences(tag)**: Total count of ground-truth keywords found within a specific HTML tag across all pages.
- **Max Occurrences**: The highest keyword occurrence count among all tags (baseline tag used for normalization; normalization range: 0–1.0).

### Normalization Approach
- **Per-Dataset**: Each dataset's scores normalized independently (accounts for dataset size/language differences).
- **Global (Cross-Dataset)**: All keyword occurrences aggregated across all 5 datasets, then normalized by the global maximum.
- **Interpretation**: A score of 1.0 = highest importance; 0.0 = no keyword occurrences detected.

---

## Global Top-10 Ranking (All Datasets Combined)

| Rank | HTML Tag          | Total Keyword Occurrences | Importance Score |
|------|-------------------|---------------------------|------------------|
| 1    | `<a>` (links)     | 12,725                    | 1.000            |
| 2    | `<p>` (paragraph) | 11,251                    | 0.884            |
| 3    | meta keywords     | 8,621                     | 0.677            |
| 4    | `<title>`         | 1,270                     | 0.100            |
| 5    | `<h1>`            | 1,111                     | 0.087            |
| 6    | URL path          | 1,078                     | 0.085            |
| 7    | `<h2>`            | 945                       | 0.074            |
| 8    | `<h3>`            | 724                       | 0.057            |
| 9    | `<strong>`        | 519                       | 0.041            |
| 10   | `<h4>`            | 340                       | 0.027            |

*Note: Tags with 0 occurrences (e.g., `<em>`, `<span>`, `<li>`) excluded from Top-10.*

---

## Key Findings & Insights

### 1. **Link Text (`<a>`) Dominates**
- **Highest importance** across all datasets, with 12,725 occurrences.
- Indicates that keywords are heavily present in hyperlinked text (navigation, related articles, references).
- **Implication**: Weighting `<a>` tags 1.0x (100%) in keyword extraction algorithms.

### 2. **Paragraph Content (`<p>`) is Critical**
- Second-highest with 11,251 occurrences (0.884 score).
- Reflects that main body text contains substantial keyword density.
- **Implication**: Assignment of 0.88x weight to `<p>` tags ensures body content is prioritized but secondary to links.

### 3. **Meta Keywords Maintain Relevance**
- 8,621 occurrences (0.677 score) despite evolving SEO practices.
- Still present and informative in modern web content.
- **Implication**: Include meta keywords extraction with ~0.68x weight.

### 4. **Headings & Title Are Secondary**
- `<title>`, `<h1>`, `<h2>`, `<h3>` combined = 4,050 occurrences (avg. 0.08 score).
- Lower than expected, possibly due to:
  - Concise nature of titles/headings (fewer words).
  - Keywords distributed across body text and links.
- **Implication**: Headings serve as secondary signals; weight them 0.08–0.10x.

### 5. **URL Paths Are Weak Indicators**
- 1,078 occurrences (0.085 score).
- Limited keyword information in URL structure.
- **Implication**: URL extraction should be a low-priority fallback (0.085x weight).

### 6. **Minimal Contribution from Emphasis Tags**
- `<strong>`, `<em>`, `<span>`: Combined 520 occurrences (<0.05 score each).
- Emphasis tags are rarely used for primary keywords in the analyzed datasets.
- **Implication**: Low weight (0.03–0.04x) or skip in algorithms.

---

## Recommended Tag Weights for Algorithms (HRank / DRank)

Based on Importance Scores:

```
<a>            → 1.00 (baseline, 100%)
<p>            → 0.88
meta_keywords → 0.68
<title>        → 0.10
<h1>           → 0.09
URL path       → 0.08
<h2>           → 0.07
<h3>           → 0.06
<strong>       → 0.04
<h4>, others   → 0.02–0.03
```

**Usage**: Multiply each tag's keyword count by its weight before aggregating scores.

---

## Consistency Notes

### Cross-Language Observations
- **English datasets** (Macworld, IndianExpress): Tend to concentrate keywords in `<a>` and `<p>` tags.
- **Finnish/German datasets** (Kaksplus, Uusisuomi, German): Similar distribution, indicating that keyword placement is relatively language-agnostic in modern HTML.
- **Recommendation**: Apply consistent weights across all languages (no language-specific adjustments needed).

### Variability & Robustness
- High occurrence counts for top 3 tags (>8,000) suggest **robust, stable rankings**.
- Lower counts for rank 4–10 (<2,000) indicate **higher sensitivity to dataset composition**, but overall pattern is consistent.

---

## Output Files Generated

1. **Global Top-10 Table** → `global_top10.csv`
   - Columns: HTML Tag, Total Keyword Occurrences, Importance Score

2. **Global Normalized Scores** → `global_normalized_scores.csv`
   - Complete list of all tags with occurrences and normalized scores.

3. **Per-Dataset Analysis** → `{Dataset}_tag_analysis.csv` (if provided)
   - Macworld, IndianExpress, Kaksplus, Uusisuomi, German

4. **Visualization** → `global_top10_plot.png`
   - Bar chart of Top-10 tags by Importance Score.

5. **Per-Dataset Comparison Chart** → `top10_per_dataset_importance.png`
   - Side-by-side comparison of tag importance across datasets.

---

## Recommendations for the Technical Report

### Section: "Scoring & Ranking (Member 3)"

**Include**:
- The Importance Score formula (as shown above).
- Global Top-10 table (copy from this document).
- Bar chart visualization (`global_top10_plot.png`).
- Key findings summary (points 1–6 above).
- Recommended weights table for HRank/DRank implementation.

**Length**: ~1–2 pages + 1 visualization.

---

## Next Steps (Members 1–4 Integration)

- **Member 4 (Report Compilation)**: Integrate this scoring section into the final technical report.
- **Member 2 (Algorithm Implementation)**: Use the recommended weights above for HRank/DRank implementations.
- **Member 1 (Data Preparation)**: Verify dataset statistics match the aggregated counts shown here.

---

**Prepared by**: Member 3 (Scoring & Ranking Lead)  
**Date**: March 4, 2026  
**Status**: ✅ Complete and ready for integration.
