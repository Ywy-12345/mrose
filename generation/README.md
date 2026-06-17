# Sequence generation

This folder contains standalone mROSE sequence-generation entry points for the three major mRNA regions:

- `5utr/generate_5utr.py`: generate and rank 5′ UTR candidates.
- `cds/generate_cds.py`: generate length-matched CDS candidates and rank them with model score, CAI, GC and optional MFE.
- `3utr/generate_3utr.py`: generate and rank 3′ UTR candidates.

The scripts were packaged from the local generation bundle and are designed to use one checkpoint per region for both candidate generation and scoring.

## Checkpoints

Large checkpoint files are intentionally excluded from Git history. For local generation, place them here:

```text
checkpoints/generation/
├── 5UTR_Model.pth
├── CDS_Model.pth
└── 3UTR_Model.pth
```

The local update created this folder from `Generate.rar`, but the `.pth` files are ignored by Git because each file is hundreds of megabytes.

## Demo

Print the dependency and checkpoint status plus ready-to-run commands:

```bash
python scripts/demo_generate_sequences.py
```

Run one demo task:

```bash
python scripts/demo_generate_sequences.py --run 5utr
python scripts/demo_generate_sequences.py --run cds
python scripts/demo_generate_sequences.py --run 3utr
```

Run all demo tasks:

```bash
python scripts/demo_generate_sequences.py --run all
```

Outputs are written under `outputs/generation/`, which is ignored by Git.

## Direct commands

5′ UTR:

```bash
python generation/5utr/generate_5utr.py \
  --checkpoint checkpoints/generation/5UTR_Model.pth \
  --input_fasta generation/examples/5utr_template.fasta \
  --num_samples 20 \
  --top_k 5 \
  --device cpu \
  --output_dir outputs/generation/5utr_demo \
  --output_prefix demo_5utr
```

CDS:

```bash
python generation/cds/generate_cds.py \
  --checkpoint checkpoints/generation/CDS_Model.pth \
  --input_fasta generation/examples/cds_template.fasta \
  --num_samples 20 \
  --top_k 5 \
  --device cpu \
  --mfe_weight 0 \
  --output_dir outputs/generation/cds_demo
```

3′ UTR:

```bash
python generation/3utr/generate_3utr.py \
  --checkpoint checkpoints/generation/3UTR_Model.pth \
  --input_fasta generation/examples/3utr_template.fasta \
  --num_samples 20 \
  --top_k 5 \
  --device cpu \
  --match_input_length \
  --output_dir outputs/generation/3utr_demo \
  --output_prefix demo_3utr
```

## Runtime notes

The generation scripts require the scientific Python stack used by mROSE, including PyTorch, NumPy, pandas, SciPy, scikit-learn, tqdm and Biopython. The 5′ UTR and 3′ UTR generators also require ViennaRNA Python bindings for MFE scoring. The CDS demo disables MFE scoring by default with `--mfe_weight 0` so it can run in environments without ViennaRNA.
