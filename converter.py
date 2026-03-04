#!/usr/bin/env python3

import argparse
from pathlib import Path
import polars as pl
import sys

EXCEL_ROW_LIMIT = 1_048_576
SUPPORTED_TYPES = {"parquet", "csv"}


def load_dataframe(file_path: Path) -> pl.DataFrame:
    """
    Load parquet or CSV file into a Polars DataFrame.
    """
    suffix = file_path.suffix.lower()

    if suffix == ".parquet":
        return pl.read_parquet(file_path)

    elif suffix == ".csv":
        return pl.read_csv(file_path)

    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def convert_to_excel(input_file: Path, output_file: Path) -> None:
    """
    Convert parquet or CSV file to Excel (.xlsx).
    """
    try:
        df = load_dataframe(input_file)

        if df.height > EXCEL_ROW_LIMIT:
            raise ValueError(
                f"{input_file} has {df.height} rows. "
                f"Excel limit is {EXCEL_ROW_LIMIT} rows."
            )

        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.write_excel(output_file, worksheet="Sheet1")

        print(f"[OK] {input_file} -> {output_file}")

    except Exception as e:
        print(f"[ERROR] {input_file}: {e}", file=sys.stderr)


def process_folder(
    input_dir: Path,
    output_dir: Path,
    recursive: bool,
    file_type: str,
) -> None:
    """
    Convert selected file types in folder to Excel.
    """
    pattern = "**/*" if recursive else "*"
    all_files = list(input_dir.glob(pattern))

    selected_files = []

    for f in all_files:
        if not f.is_file():
            continue

        suffix = f.suffix.lower().lstrip(".")

        if file_type == "all" and suffix in SUPPORTED_TYPES:
            selected_files.append(f)
        elif file_type in SUPPORTED_TYPES and suffix == file_type:
            selected_files.append(f)

    if not selected_files:
        print(f"No matching '{file_type}' files found.")
        return

    for file_path in selected_files:
        relative_path = file_path.relative_to(input_dir)
        output_file = output_dir / relative_path.with_suffix(".xlsx")
        convert_to_excel(file_path, output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Convert parquet and/or CSV files in a folder to Excel."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input folder containing files",
    )

    parser.add_argument(
        "output",
        type=Path,
        help="Output folder for Excel files",
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively search for files",
    )

    parser.add_argument(
        "-t",
        "--type",
        choices=["parquet", "csv", "all"],
        default="all",
        help="Select file type to convert (default: all)",
    )

    args = parser.parse_args()

    if not args.input.exists() or not args.input.is_dir():
        print("Input folder does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    process_folder(
        input_dir=args.input,
        output_dir=args.output,
        recursive=args.recursive,
        file_type=args.type,
    )


if __name__ == "__main__":
    main()
