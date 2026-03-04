#!/usr/bin/env python3
"""Scoring and ranking script for Member 3.

Reads tag count CSVs (tag_counts_*.csv) or processes the dataset directly if needed.
Normalizes counts, computes Importance Score, and exports Top 10 lists.
"""
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import os

try:
    from bs4 import BeautifulSoup
except Exception:
    BeautifulSoup = None

# base directory containing the extracted datasets (repo-relative)
HERE = Path(__file__).resolve().parent
BASE = HERE / "Datasets"

# output folder
out_dir = HERE / "member3_outputs"
out_dir.mkdir(parents=True, exist_ok=True)

# helper: common tags to inspect
INTEREST_TAGS = [
    "title",
    "h1",
    "h2",
    "h3",
    "p",
    "a",
    "li",
    "span",
    "strong",
    "em",
    "meta",
    "img",
]


def generate_tag_counts_for_dataset(dataset_path: Path, output_dir: Path):
    """Scan dataset folder for per-document HTML.txt and GT.txt, count keyword occurrences per tag.

    Writes a CSV `tag_counts_{dataset}.csv` into `output_dir` and returns a DataFrame.
    """
    rows = []
    counts = {}
    # initialize counts
    for t in INTEREST_TAGS:
        counts[t] = 0

    if not dataset_path.exists():
        return pd.DataFrame()

    # iterate document subfolders (skip nested dataset folders)
    for child in sorted(dataset_path.iterdir()):
        if not child.is_dir():
            continue
        html_file = child / "HTML.txt"
        gt_file = child / "GT.txt"
        if not html_file.exists() or not gt_file.exists():
            continue
        try:
            html = html_file.read_text(encoding="utf-8", errors="ignore")
            gt_lines = [l.strip() for l in gt_file.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip()]
        except Exception:
            continue

        if BeautifulSoup is None:
            raise RuntimeError("BeautifulSoup (bs4) is required to parse HTML. Install with `pip install beautifulsoup4`.")

        soup = BeautifulSoup(html, "html.parser")
        # prepare lower-case GT keywords
        kws = [k.lower() for k in gt_lines]

        # count occurrences per tag for all keywords
        for tag in INTEREST_TAGS:
            if tag == "meta":
                # check meta content attributes
                for m in soup.find_all("meta"):
                    content = (m.get("content") or "") + " " + (m.get("name") or "")
                    content_l = content.lower()
                    for kw in kws:
                        counts["meta"] += content_l.count(kw)
            elif tag == "img":
                for im in soup.find_all("img"):
                    alt = (im.get("alt") or "").lower()
                    for kw in kws:
                        counts["img"] += alt.count(kw)
            else:
                for el in soup.find_all(tag):
                    text = (el.get_text(separator=" ") or "").lower()
                    for kw in kws:
                        counts[tag] += text.count(kw)

    # transform to DataFrame
    for tag, cnt in counts.items():
        rows.append({"HTML Tag": tag, "Occurrences": int(cnt)})

    df = pd.DataFrame(rows)
    # ensure deterministic order
    df = df.sort_values("Occurrences", ascending=False).reset_index(drop=True)
    dataset_name = dataset_path.name
    out_csv = output_dir / f"tag_counts_{dataset_name}.csv"
    df.to_csv(out_csv, index=False)
    return df


# look for per-dataset CSVs first (in repo Datasets and outputs)
csvs = sorted(BASE.glob("tag_counts_*.csv")) + sorted(out_dir.glob("tag_counts_*.csv"))

# if none found, attempt to auto-generate by scanning dataset folders inside `BASE`
if not csvs:
    if not BASE.exists():
        print("Datasets folder not found at:", BASE)
        csvs = []
    else:
        # generate for each top-level dataset directory
        for ds in sorted(BASE.iterdir()):
            if not ds.is_dir():
                continue
            # skip nested 'german_dataset' leaf inside dataset root if present
            # if the dataset contains many numeric child folders, we treat ds as dataset
            try:
                df_ds = generate_tag_counts_for_dataset(ds, out_dir)
                if not df_ds.empty:
                    csvs.append(out_dir / f"tag_counts_{ds.name}.csv")
            except RuntimeError as e:
                print(e)
                print("Install BeautifulSoup4 and re-run: pip install beautifulsoup4")
                break

all_rows = []
for csv in csvs:
    try:
        df = pd.read_csv(csv, encoding="utf-8")
    except Exception:
        continue
    # normalize column names
    if "HTML Tag" not in df.columns:
        if "tag" in df.columns:
            df = df.rename(columns={"tag": "HTML Tag"})
        elif "Tag" in df.columns:
            df = df.rename(columns={"Tag": "HTML Tag"})
    if "Occurrences" not in df.columns:
        if "count" in df.columns:
            df = df.rename(columns={"count": "Occurrences"})
    csv_name = csv.stem.replace("tag_counts_", "")
    df["Occurrences"] = pd.to_numeric(df["Occurrences"].fillna(0), errors="coerce").fillna(0).astype(int)
    total = df["Occurrences"].sum()
    max_occ = df["Occurrences"].max() if not df.empty else 1
    df["Percentage"] = (df["Occurrences"] / total * 100).fillna(0)
    df["Importance Score"] = (df["Occurrences"] / max_occ).fillna(0)
    df["Dataset"] = csv_name
    all_rows.append(df[["Dataset", "HTML Tag", "Occurrences", "Percentage", "Importance Score"]])

if all_rows:
    df_all = pd.concat(all_rows, ignore_index=True)
    combined_csv = out_dir / "member3_normalized_scores.csv"
    df_all.to_csv(combined_csv, index=False)
    top10_per = df_all.sort_values(["Dataset", "Occurrences"], ascending=[True, False]).groupby("Dataset").head(10)
    top10_per.to_csv(out_dir / "member3_top10_per_dataset.csv", index=False)
    # global aggregation
    global_df = df_all.groupby("HTML Tag", as_index=False).agg({"Occurrences": "sum"})
    global_df["Percentage"] = (global_df["Occurrences"] / global_df["Occurrences"].sum() * 100).fillna(0)
    global_max = global_df["Occurrences"].max() if not global_df.empty else 1
    global_df["Importance Score"] = (global_df["Occurrences"] / global_max).fillna(0)
    global_df = global_df.sort_values("Occurrences", ascending=False)
    global_df.to_csv(out_dir / "member3_top10_global.csv", index=False)
    global_df.head(10).to_csv(out_dir / "member3_top10_global_head10.csv", index=False)
    # plots
    try:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=top10_per, x="HTML Tag", y="Importance Score", hue="Dataset")
        plt.xticks(rotation=45)
        plt.title("Top tags (Importance Score) per dataset")
        plt.tight_layout()
        plt.savefig(out_dir / "top10_per_dataset_importance.png", dpi=200)
        plt.clf()
        plt.figure(figsize=(10, 5))
        sns.barplot(data=global_df.head(10), x="HTML Tag", y="Importance Score", palette="viridis")
        plt.xticks(rotation=45)
        plt.title("Global Top-10 Tags (Importance Score)")
        plt.tight_layout()
        plt.savefig(out_dir / "global_top10_importance.png", dpi=200)
    except Exception:
        print("Plotting failed (matplotlib/seaborn issue), but CSV outputs are available in", out_dir)
    print("Outputs written to", out_dir)
else:
    print("No data processed; please ensure dataset folders contain HTML.txt and GT.txt per document.")
