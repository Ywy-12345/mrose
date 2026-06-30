import argparse
from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mrose.full_length_fusion import (  # noqa: E402
    infer_max_lens_from_dataset,
    train_master_model,
)


DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "example" / "in_solution_half_life"
DEFAULT_MODEL_DIR = PROJECT_ROOT / "outputs" / "full_length_stability" / "in_solution_half_life"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train the full-length mRNA stability model on in_solution_half_life."
    )
    parser.add_argument("--data_dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--model_dir", type=Path, default=DEFAULT_MODEL_DIR)
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--length_percentile", type=float, default=0.90)
    parser.add_argument("--bucket_size", type=int, default=16)
    parser.add_argument("--cap_5utr", type=int, default=128)
    parser.add_argument("--cap_cds", type=int, default=512)
    parser.add_argument("--cap_3utr", type=int, default=512)
    return parser.parse_args()


def validate_args(args):
    if args.epochs <= 0 or args.epochs % 10 != 0:
        raise ValueError("--epochs must be a positive multiple of 10")
    if not 0 < args.length_percentile <= 1:
        raise ValueError("--length_percentile must be in the interval (0, 1]")
    if args.bucket_size <= 0:
        raise ValueError("--bucket_size must be positive")
    if min(args.cap_5utr, args.cap_cds, args.cap_3utr) <= 0:
        raise ValueError("All sequence-length caps must be positive")


def main():
    args = parse_args()
    validate_args(args)

    train_csv = args.data_dir / "train.csv"
    dev_csv = args.data_dir / "dev.csv"
    test_csv = args.data_dir / "test.csv"

    missing_files = [path for path in (train_csv, test_csv) if not path.is_file()]
    if missing_files:
        missing = ", ".join(str(path) for path in missing_files)
        raise FileNotFoundError(f"Missing required dataset file(s): {missing}")

    args.model_dir.mkdir(parents=True, exist_ok=True)

    max_len_5, max_len_c, max_len_3, length_stats = infer_max_lens_from_dataset(
        csv_paths=[str(train_csv)],
        percentile=args.length_percentile,
        bucket_size=args.bucket_size,
        min_len_5=16,
        min_len_c=16,
        min_len_3=16,
        cap_5=args.cap_5utr,
        cap_c=args.cap_cds,
        cap_3=args.cap_3utr,
        verbose=True,
    )

    final_model_path = args.model_dir / (
        f"model_5U{max_len_5}_C{max_len_c}_3U{max_len_3}_"
        f"final_epoch_{args.epochs}.pth"
    )

    metrics = train_master_model(
        MAX_LEN_5=max_len_5,
        MAX_LEN_C=max_len_c,
        MAX_LEN_3=max_len_3,
        train_csv=str(train_csv),
        val_csv=str(dev_csv) if dev_csv.is_file() else None,
        test_csv=str(test_csv),
        final_model_path=str(final_model_path),
        EPOCHS=args.epochs,
    )

    validation_metrics = metrics["validation"] or {
        "mse": float("nan"),
        "pearson": float("nan"),
        "r2": float("nan"),
    }
    test_metrics = metrics["test"]
    log_entry = {
        "Dataset": "in_solution_half_life",
        "Epochs": args.epochs,
        "5UTR_Len": max_len_5,
        "CDS_Len": max_len_c,
        "3UTR_Len": max_len_3,
        "5UTR_Max_Raw": length_stats["5UTR"]["max"],
        "CDS_Max_Raw": length_stats["CDS_codons"]["max"],
        "3UTR_Max_Raw": length_stats["3UTR"]["max"],
        "Length_Percentile": args.length_percentile,
        "Final_Val_MSE": validation_metrics["mse"],
        "Final_Val_Pearson": validation_metrics["pearson"],
        "Final_Val_R2": validation_metrics["r2"],
        "Final_Test_MSE": test_metrics["mse"],
        "Final_Test_Pearson": test_metrics["pearson"],
        "Final_Test_R2": test_metrics["r2"],
        "Checkpoint": str(final_model_path),
    }
    pd.DataFrame([log_entry]).to_csv(args.model_dir / "training_log.csv", index=False)

    print(f"Final-epoch model saved to: {final_model_path}")


if __name__ == "__main__":
    main()
