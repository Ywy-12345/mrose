# Full-length mRNA stability regression example

**Task type:** regression.  
**Biological target:** full-length mRNA phenotype such as in-solution half-life.  
**Source-style data:** each task folder contains `train.csv`, `dev.csv` and `test.csv` with `sequence` and `label` columns.

```text
experiments/full_length_stability/example/in_solution_half_life/
├── train.csv
├── dev.csv
└── test.csv
```

Run from the repository root:

```bash
bash experiments/full_length_stability/example/run_example.sh
```

The dedicated training entry point defaults to
`experiments/full_length_stability/example/in_solution_half_life`. It trains
one model from scratch using `train.csv`, keeps `dev.csv` separate for
validation, evaluates `test.csv` every 10 epochs, and saves only the final
epoch checkpoint. The default epoch count is 40 and must remain a positive
multiple of 10.

Hyperparameters can be overridden directly without a parameter grid:

```bash
python experiments/full_length_stability/train_full_length_stability.py \
  --epochs 40 \
  --length_percentile 0.90 \
  --cap_5utr 128 \
  --cap_cds 512 \
  --cap_3utr 512
```

The full-length loader automatically segments a transcript into 5′UTR, CDS and 3′UTR using the first `ATG` and the first in-frame stop codon after it.
