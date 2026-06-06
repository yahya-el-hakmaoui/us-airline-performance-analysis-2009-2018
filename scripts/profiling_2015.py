# Author: TAHA

import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# =========================
# LOAD .ENV
# =========================

load_dotenv(find_dotenv())

DATA_RAW_PATH = os.getenv("DATA_RAW_PATH")
REPORTS_PROFILING_PATH = os.getenv("REPORTS_PROFILING_PATH")

if not DATA_RAW_PATH:
    raise ValueError("DATA_RAW_PATH not found in .env")

if not REPORTS_PROFILING_PATH:
    raise ValueError("REPORTS_PROFILING_PATH not found in .env")

# =========================
# BASE DIRECTORY
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]

csv_file = BASE_DIR / DATA_RAW_PATH / "2015.csv"

report_dir = BASE_DIR / REPORTS_PROFILING_PATH
report_dir.mkdir(parents=True, exist_ok=True)

report_file = report_dir / "profiling_2015.html"

# =========================
# READ CSV
# =========================

print("Reading:", csv_file)

df = pd.read_csv(csv_file)

# checking the dataset:lignes,colonnes,types

print(df.shape)
print(df.info())
print(df.head())

# =========================
# PROFILING
# =========================

from ydata_profiling import ProfileReport

profile = ProfileReport(
    df,
    minimal=False
)

profile.to_file(str(report_file))

print("Profiling saved to:", report_file)

# =========================
# ANALYSE MANUELLE CDC
# =========================

cause_cols = [
    "CARRIER_DELAY",
    "WEATHER_DELAY",
    "NAS_DELAY",
    "SECURITY_DELAY",
    "LATE_AIRCRAFT_DELAY"
]

for c in cause_cols:
    print(f"{c}: {df[c].isna().mean()*100:.2f}%")

# Distribution ARR_DELAY

print(df["ARR_DELAY"].describe())

# Vérification ARR_DEL15

df["ARR_DEL15"] = (df["ARR_DELAY"] > 15).astype(int)

errors = df[
    (df["ARR_DELAY"] > 15)
    &
    (df["ARR_DEL15"] != 1)
]

print("Errors shape:", errors.shape)