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

# base directory containing the extracted datasets
BASE = "/Users/rexoghenerobo/Downloads/Datasets"

# output folder
out_dir = Path(BASE) / "member3_outputs"
out_dir.mkdir(exist_ok=True)

# look for per-dataset CSVs
csvs = sorted(Path(BASE).glob("tag_counts_*.csv"))

# if none found, we could generate from scratch by running notebook or other script
if not csvs:
    print("No tag_counts_*.csv files found in", BASE)
    print("Please run the notebook to produce per-dataset counts or create such files.")
    # exit without error so notebooks can continue
    csvs = []

all_rows = []
for csv in csvs:
    df = pd.read_csv(csv, encoding="utf-8")
    # normalize column names
    if "HTML Tag" not in df.columns:
        if "tag" in df.columns:
            df = df.rename(columns={"tag":"HTML Tag"})
        elif "Tag" in df.columns:
            df = df.rename(columns={"Tag":"HTML Tag"})
    if "Occurrences" not in df.columns:
        if "count" in df.columns:
            df = df.rename(columns={"count":"Occurrences"})
    csv_name = csv.stem.replace("tag_counts_","")
    df["Occurrences"] = pd.to_numeric(df["Occurrences"].fillna(0), errors="coerce").fillna(0).astype(int)
    max_occ = df["Occurrences"].max() if not df.empty else 1
    df["Percentage"] = (df["Occurrences"] / df["Occurrences"].sum() * 100).fillna(0)
    df["Importance Score"] = (df["Occurrences"] / max_occ).fillna(0)
    df["Dataset"] = csv_name
    all_rows.append(df[["Dataset","HTML Tag","Occurrences","Percentage","Importance Score"]])

if all_rows:
    df_all = pd.concat(all_rows, ignore_index=True)
    combined_csv = out_dir / "member3_normalized_scores.csv"
    df_all.to_csv(combined_csv, index=False)
    top10_per = df_all.sort_values(["Dataset","Occurrences"], ascending=[True,False]).groupby("Dataset").head(10)
    top10_per.to_csv(out_dir / "member3_top10_per_dataset.csv", index=False)
    # global aggregation
    global_df = df_all.groupby("HTML Tag", as_index=False).agg({"Occurrences":"sum"})
    global_df["Percentage"] = (global_df["Occurrences"] / global_df["Occurrences"].sum() * 100).fillna(0)
    global_max = global_df["Occurrences"].max() if not global_df.empty else 1
    global_df["Importance Score"] = (global_df["Occurrences"] / global_max).fillna(0)
    global_df = global_df.sort_values("Occurrences", ascending=False)
    global_df.to_csv(out_dir / "member3_top10_global.csv", index=False)
    global_df.head(10).to_csv(out_dir / "member3_top10_global_head10.csv", index=False)
    # plots
    plt.figure(figsize=(12,6))
    sns.barplot(data=top10_per, x="HTML Tag", y="Importance Score", hue="Dataset")
    plt.xticks(rotation=45)
    plt.title("Top tags (Importance Score) per dataset")
    plt.tight_layout()
    plt.savefig(out_dir / "top10_per_dataset_importance.png", dpi=200)
    plt.clf()
    plt.figure(figsize=(10,5))
    sns.barplot(data=global_df.head(10), x="HTML Tag", y="Importance Score", palette="viridis")
    plt.xticks(rotation=45)
    plt.title("Global Top-10 Tags (Importance Score)")
    plt.tight_layout()
    plt.savefig(out_dir / "global_top10_importance.png", dpi=200)
    print("Outputs written to", out_dir)
else:
    print("No data processed; please ensure tag count CSVs exist or run notebook cells first.")
