"""
generate_data.py
Generates two datasets:
  1. student_performance.csv  – 1 200 students, seed 55
  2. duka_sales.csv           – Duka Electronics H1-2026, seed 2026
Run once before opening either notebook.
"""

import numpy as np
import pandas as pd

# ── Engagement 1 · Student Performance ──────────────────────────────────────
rng = np.random.default_rng(55)

n = 1200
genders      = rng.choice(["Male", "Female"], size=n, p=[0.50, 0.50])
school_types = rng.choice(["Public", "Private"], size=n, p=[0.65, 0.35])
counties     = rng.choice(
    ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
     "Thika",   "Nyeri",   "Meru",   "Kakamega", "Garissa"],
    size=n,
)

study_hours  = np.clip(rng.normal(4.5, 1.8, n), 0.5, 10.0).round(1)
attendance   = np.clip(rng.normal(78, 12, n), 30, 100).round(1)

# Scores correlated with study_hours and attendance
base  = 40 + 3.5 * study_hours + 0.25 * attendance
noise = rng.normal(0, 8, n)
private_boost = np.where(school_types == "Private", 5, 0)
gender_shift  = np.where(genders == "Female", 2, 0)

math_score    = np.clip(base + noise + private_boost + gender_shift + rng.normal(0, 4, n), 0, 100).round(1)
english_score = np.clip(base + noise + private_boost + gender_shift + rng.normal(0, 4, n), 0, 100).round(1)
science_score = np.clip(base + noise + private_boost + gender_shift + rng.normal(0, 4, n), 0, 100).round(1)

student_df = pd.DataFrame({
    "student_id":    range(1001, 1001 + n),
    "gender":        genders,
    "school_type":   school_types,
    "county":        counties,
    "study_hours":   study_hours,
    "attendance_pct": attendance,
    "math_score":    math_score,
    "english_score": english_score,
    "science_score": science_score,
})

student_df.to_csv("student_performance.csv", index=False)
print(f"student_performance.csv written  ({len(student_df)} rows)")

# ── Engagement 2 · Duka Electronics Sales ───────────────────────────────────
rng2 = np.random.default_rng(2026)

n2 = 1800
dates = pd.date_range("2026-01-01", "2026-06-30", freq="D")
sale_dates = rng2.choice(dates, size=n2)

categories  = rng2.choice(
    ["Phones", "Laptops", "TVs", "Accessories", "Audio"],
    size=n2, p=[0.30, 0.25, 0.20, 0.15, 0.10],
)
regions = rng2.choice(
    ["Nairobi", "Coast", "Rift Valley", "Western", "Central"],
    size=n2, p=[0.35, 0.20, 0.20, 0.15, 0.10],
)
sales_reps = rng2.choice(
    ["Alice", "Bob", "Carol", "David", "Eve", "Frank"],
    size=n2,
)

unit_prices = {
    "Phones": 35000, "Laptops": 75000, "TVs": 55000,
    "Accessories": 2500, "Audio": 8000,
}
units_sold = rng2.integers(1, 15, size=n2)
price_arr  = np.array([unit_prices[c] for c in categories])
noise2     = rng2.normal(1.0, 0.12, n2)
revenue    = (price_arr * units_sold * noise2).round(0).astype(int)
cogs       = (revenue * rng2.uniform(0.45, 0.65, n2)).round(0).astype(int)
profit     = revenue - cogs

duka_df = pd.DataFrame({
    "date":       pd.to_datetime(sale_dates),
    "category":   categories,
    "region":     regions,
    "sales_rep":  sales_reps,
    "units_sold": units_sold,
    "revenue":    revenue,
    "cogs":       cogs,
    "gross_profit": profit,
})
duka_df["month"] = duka_df["date"].dt.month_name()
duka_df["week"]  = duka_df["date"].dt.isocalendar().week.astype(int)
duka_df = duka_df.sort_values("date").reset_index(drop=True)

duka_df.to_csv("duka_sales.csv", index=False)
print(f"duka_sales.csv written  ({len(duka_df)} rows)")
