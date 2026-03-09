# HTML Tag Importance Analysis – Project 1

**Member 3: Scoring & Ranking Lead**  
**Date Completed:** March 9, 2026  
**Status:** ✅ All tasks complete – ready for team integration & final report

## Objective
Analyze keyword distribution across HTML tags in 5 datasets (English, Finnish, German) to compute normalized importance scores (0.0–1.0) and rank the top 10 most valuable tags for keyword extraction.

## Key Metrics
- Total articles analyzed: **1,019**  
- Datasets: **5** (Macworld 204, IndianExpress 329, Kaksplus 200, Uusisuomi 200, German 86)  
- Tags scored: **31**  
- Importance range: **0.04 to 100.0** (26,000× difference between top and bottom)

## Core Deliverables (in member3_outputs/)
| File | Description | Use in Report |
|------|-------------|---------------|
| global_tag_frequency.csv | Raw counts, percentages, importance scores (all tags) | Results table / appendix |
| global_normalized_scores.csv | Ranked importance scores | Main results section |
| MEMBER3_Top10_Ranking.csv | Top-10 tags with ranks & scores | Key figure / table |
| dataset_comparison_chart.png | Bar chart comparing scores across datasets | Visualization |
| global_top10_importance.png | Global top-10 bar chart | Visualization |
| HANDOFF_TO_MEMBER4.md | Handover summary & next steps | Read first |
| MEMBER3_METHODOLOGY.md | Scoring formula & logic explanation | Methodology section |

**All CSVs open cleanly in Excel/Google Sheets. Charts are high-quality PNGs.**

## Key Findings (one sentence)
Structural HTML tags (div, a, li, span) are **1,000× more important** for keyword extraction than formatting tags (em, strong), based on 1,019 webpages across 5 diverse datasets.

## Recommended Tag Weights for Algorithm (Phase 2)
For HRank/DRank implementation (Member 2):

```python
TAG_IMPORTANCE = {
    'div': 1.00,
    'a': 0.99,
    'p': 0.89,
    'meta_keywords': 0.59,
    'title': 0.09,
    # ... add more from global_normalized_scores.csv
    'strong': 0.04,
    'em': 0.02
}

# Example weighting
keyword_score = base_score * TAG_IMPORTANCE.get(html_tag, 0.1)