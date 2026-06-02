import argparse
import os
from pathlib import Path
import sys

try:
    from dotenv import load_dotenv, find_dotenv
except Exception:
    print("Please install python-dotenv (pip install python-dotenv)")
    raise

load_dotenv(find_dotenv())

DATA_RAW_PATH = os.getenv("DATA_RAW_PATH")
DATA_PARQUET_RAW_PATH = os.getenv("DATA_PARQUET_RAW_PATH")

if not DATA_RAW_PATH:
    print("ERROR: DATA_RAW_PATH is not set in the environment (.env)")
    sys.exit(2)

if not DATA_PARQUET_RAW_PATH:
    print("ERROR: DATA_PARQUET_RAW_PATH is not set in the environment (.env)")
    sys.exit(2)

DATA_RAW = Path(DATA_RAW_PATH)
PARQUET_RAW = Path(DATA_PARQUET_RAW_PATH)

def find_csv_files(directory: Path):
    if not directory.exists():
        return []
    return sorted(directory.glob("*.csv"))


def convert_csv_to_parquet(csv_path: Path, parquet_path: Path, overwrite: bool = False, chunksize: int = 100_000):
    """Convert a single CSV to Parquet using pyarrow ParquetWriter and pandas chunks.

    Returns True on success, False on failure or if skipped.
    """
    try:
        import polars as pl
    except Exception:
        print("Missing dependency: polars is required. Install with: pip install polars")
        raise

    if parquet_path.exists() and not overwrite:
        print(f"Skipping existing: {parquet_path}")
        return False

    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    # Use a LazyFrame scan to enable streaming collection which is memory-efficient.
    lf = pl.scan_csv(str(csv_path))

    # Determine column names via schema to avoid expensive resolution warning.
    try:
        schema = lf.collect_schema()
        col_names = schema.names()
    except Exception:
        # fallback to resolving columns if collect_schema fails
        col_names = lf.columns

    # If a known column has mixed types, cast it explicitly to string to avoid surprises.
    if 'CANCELLATION_CODE' in col_names:
        lf = lf.with_columns(pl.col('CANCELLATION_CODE').cast(pl.Utf8))

    # Collect using the streaming engine to keep memory usage low.
    df = lf.collect(engine="streaming")

    # Write parquet with snappy compression.
    df.write_parquet(str(parquet_path), compression='snappy')

    # Report number of rows written if available
    try:
        rows = df.shape[0]
    except Exception:
        rows = 'unknown'

    print(f"Wrote {parquet_path} ({rows} rows)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Convert CSV files to Parquet using .env paths")
    parser.add_argument("--dry-run", action="store_true", help="Show planned conversions without writing files")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing parquet files")
    parser.add_argument("--chunksize", type=int, default=100_000, help="CSV read chunksize (rows)")
    args = parser.parse_args()

    csv_files = find_csv_files(DATA_RAW)
    if not csv_files:
        print(f"No CSV files found in {DATA_RAW}")
        sys.exit(0)

    print(f"Found {len(csv_files)} CSV files in {DATA_RAW}")
    planned = []

    for csv in csv_files:
        parquet_file = PARQUET_RAW / (csv.stem + ".parquet")
        planned.append((csv, parquet_file))

    if args.dry_run:
        print("Dry run: the following conversions would be performed:")
        for src, dst in planned:
            print(f"  {src} -> {dst}")
        return

    successes = 0
    skipped = 0
    failures = 0

    for src, dst in planned:
        try:
            ok = convert_csv_to_parquet(src, dst, overwrite=args.overwrite, chunksize=args.chunksize)
            if ok:
                successes += 1
            else:
                skipped += 1
        except Exception as exc:
            print(f"Failed to convert {src}: {exc}")
            failures += 1

    print("\nSummary:")
    print(f"  Converted : {successes}")
    print(f"  Skipped   : {skipped}")
    print(f"  Failed    : {failures}")

if __name__ == '__main__':
    main()
