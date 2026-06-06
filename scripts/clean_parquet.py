import polars as pl
from pathlib import Path

# =========================
# BASE PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_DIR = BASE_DIR / "data/parquet_raw"
OUTPUT_DIR = BASE_DIR / "data/parquet_clean"
REPORT_DIR = BASE_DIR / "reports"
COHERENCE_FILE = REPORT_DIR / "coherence_errors.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# STEP 4: ERROR LOG
# =========================
violations = []

# =========================
# STEP 3: LIST FILES
# =========================
files = sorted(INPUT_DIR.glob("*.parquet"))

if not files:
    print(f"No parquet files found in {INPUT_DIR}")
    exit(0)

print(f"Found {len(files)} parquet files")

# =========================
# STEP 5: LOOP PER YEAR
# =========================
for file in files:
    print(f"\nProcessing {file.name}")

    df = pl.read_parquet(file)

    # =========================
    # STEP 6: KEEP CANCELLED (DO NOTHING)
    # =========================

    # =========================
    # STEP 7: IS_DELAYED_ARR
    # =========================
    df = df.with_columns(
        (pl.col("ARR_DELAY") > 0).alias("IS_DELAYED_ARR")
    )

    # =========================
    # STEP 8: FILL NULL CAUSES
    # =========================
    cause_cols = [
        "CARRIER_DELAY",
        "WEATHER_DELAY",
        "NAS_DELAY",
        "SECURITY_DELAY",
        "LATE_AIRCRAFT_DELAY"
    ]

    for c in cause_cols:
        df = df.with_columns(pl.col(c).fill_null(0))

    # =========================
    # STEP 9: ind1
    # =========================
    df = df.with_columns(
        (pl.col("ARR_DELAY") <= 0)
        .cast(pl.Int8)
        .alias("ind1")
    )

    # =========================
    # STEP 10:ind2
    # =========================
    df = df.with_columns(
        (pl.col("ARR_DELAY") <= 30)
        .cast(pl.Int8)
        .alias("ind2")
    )

    # =========================
    # STEP 11: COHERENCE CHECK
    # =========================
    sum_causes = (
        pl.col("CARRIER_DELAY")
        + pl.col("WEATHER_DELAY")
        + pl.col("NAS_DELAY")
        + pl.col("SECURITY_DELAY")
        + pl.col("LATE_AIRCRAFT_DELAY")
    )

    df = df.with_columns(
        sum_causes.alias("SUM_CAUSES")
    )

    df = df.with_columns(
        (pl.col("ARR_DELAY") - pl.col("SUM_CAUSES")).abs().alias("DIFF_CHECK")
    )

    bad_rows = df.filter(pl.col("DIFF_CHECK") >= 0.01)

    if bad_rows.height > 0:
        violations.append(
            bad_rows.select([
                "FL_DATE",
                "ARR_DELAY",
                "SUM_CAUSES",
                "DIFF_CHECK"
            ])
        )

    # =========================
    # STEP 13: SAVE CLEAN PARQUET
    # =========================
    output_file = OUTPUT_DIR / f"{file.stem}_clean.parquet"

    df.write_parquet(output_file, compression="snappy")

    print(f"Saved -> {output_file}")


print("\nDONE CLEANING PIPELINE")