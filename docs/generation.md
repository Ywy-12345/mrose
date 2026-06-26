# Sequence generation

mROSE provides standalone generation entry points for the three major mRNA
regions and for full-length mRNA assembly.

## What each generator does

| Region | Script | Main output |
|---|---|---|
| 5′ UTR | `generation/5utr/generate_5utr.py` | ranked 5′ UTR candidates with predicted MRL, MFE, GC and upstream AUG/ORF features |
| CDS | `generation/cds/generate_cds.py` | length-matched CDS candidates ranked by model score, CAI, GC and optional MFE |
| 3′ UTR | `generation/3utr/generate_3utr.py` | ranked 3′ UTR candidates with degradation-style prediction, MFE, GC/TC and motif features |
| Full-length mRNA | `generation/full_length/generate_full_length.py` | full transcripts assembled from generated 5′ UTR, CDS and 3′ UTR candidates |

## Recommended workflow

1. Install the environment and download checkpoints with Git LFS.
2. Run `python scripts/generate_sequences.py` to check dependencies and
   checkpoint availability.
3. Run one compact regional example.
4. Inspect the `top` CSV file under `outputs/generation/`.
5. Move to full-length generation after the regional examples work.

## Checkpoints

The released generation checkpoints are tracked with Git LFS:

```text
generation/
├── 5utr/Model.pth
├── cds/Model.pth
└── 3utr/Model.pth
```

If generation fails while loading a checkpoint, first confirm that Git LFS
downloaded the real model files rather than pointer files:

```bash
git lfs install
git lfs pull
shasum -a 256 -c MODEL_CHECKSUMS.sha256
```

## Compact examples

Print dependency and checkpoint status plus ready-to-run commands:

```bash
python scripts/generate_sequences.py
```

Run one example task:

```bash
python scripts/generate_sequences.py --run 5utr
python scripts/generate_sequences.py --run cds
python scripts/generate_sequences.py --run 3utr
python scripts/generate_sequences.py --run full_length
```

Run all example tasks:

```bash
python scripts/generate_sequences.py --run all
```

Outputs are written under `outputs/generation/`, which is ignored by Git.

## Regional direct commands

### 5′ UTR

```bash
python generation/5utr/generate_5utr.py \
  --checkpoint generation/5utr/Model.pth \
  --input_fasta generation/examples/5utr_template.fasta \
  --num_samples 20 \
  --top_k 5 \
  --device cpu \
  --output_dir outputs/generation/5utr_example \
  --output_prefix example_5utr
```

### CDS

```bash
python generation/cds/generate_cds.py \
  --checkpoint generation/cds/Model.pth \
  --input_fasta generation/examples/cds_template.fasta \
  --num_samples 20 \
  --top_k 5 \
  --device cpu \
  --mfe_weight 0 \
  --output_dir outputs/generation/cds_example
```

The CDS generator preserves the encoded protein sequence while searching
synonymous coding-sequence space.

### 3′ UTR

```bash
python generation/3utr/generate_3utr.py \
  --checkpoint generation/3utr/Model.pth \
  --input_fasta generation/examples/3utr_template.fasta \
  --num_samples 20 \
  --top_k 5 \
  --device cpu \
  --output_dir outputs/generation/3utr_example \
  --output_prefix example_3utr
```

By default, 3′ UTR candidates are allowed to vary in length. Add
`--match_input_length` only if you specifically need legacy input-length
matching.

## Full-length mRNA generation

The full-length launcher runs the three regional generators and merges
same-rank candidates into full transcripts.

### Mode 1: single full-length input

This is the recommended mode. Provide one FASTA containing a full mRNA sequence.
The script automatically splits it into 5′ UTR, CDS and 3′ UTR by ORF detection
(ATG to the first downstream in-frame stop codon), then runs each regional
generator:

```bash
python generation/full_length/generate_full_length.py \
  --full_mrna_fasta generation/examples/full_mrna_template.fasta \
  --num_samples 20 \
  --top_k 5 \
  --device cpu \
  --output_dir outputs/generation/full_length_example \
  --output_prefix example_full_length
```

Splitting logic:

```text
Input: AGGAATAA...CCACC ATG ... CDS ... TAA GCTGCC...TAAA
                     |      |            |
                     5′ UTR  CDS         3′ UTR
```

- 5′ UTR: everything before the first ATG.
- CDS: from ATG through the first downstream in-frame stop codon.
- 3′ UTR: everything after the stop codon.

If no ATG is found, the first third is used as 5′ UTR. If no in-frame stop
codon is found, the CDS is truncated to a length divisible by 3.

### Mode 2: separate regional inputs

Use this mode when the 5′ UTR, CDS and 3′ UTR templates are already stored as
separate FASTA files:

```bash
python generation/full_length/generate_full_length.py \
  --five_utr_fasta generation/examples/5utr_template.fasta \
  --cds_fasta generation/examples/cds_template.fasta \
  --three_utr_fasta generation/examples/3utr_template.fasta \
  --num_samples 20 \
  --top_k 5 \
  --device cpu \
  --output_dir outputs/generation/full_length_example \
  --output_prefix example_full_length
```

Merging is rank-wise:

```text
full_length_rank_1 = 5utr_generated_rank_1 + cds_generated_rank_1 + 3utr_generated_rank_1
full_length_rank_2 = 5utr_generated_rank_2 + cds_generated_rank_2 + 3utr_generated_rank_2
```

## Output files

Regional generation writes CSV and FASTA outputs under the requested output
directory. The `top` CSV is the primary result file for most users.

Full-length generation writes regional subdirectories plus merged full-length
outputs:

```text
outputs/generation/full_length_example/
├── split_input/                       # only for single full-length input mode
├── 5utr/
├── cds/
├── 3utr/
├── example_full_length_top5.csv
└── example_full_length_top5.fasta
```

The merged CSV includes:

- `rank`
- `sequence`
- `five_utr_sequence`, `cds_sequence`, `three_utr_sequence`
- `five_utr_length`, `cds_length`, `three_utr_length`, `full_length`
- `five_utr_score`, `cds_score`, `three_utr_score`

## Runtime notes

The generation scripts require the scientific Python stack used by mROSE,
including PyTorch, NumPy, pandas, SciPy, scikit-learn, tqdm and Biopython.
The 5′ UTR and 3′ UTR generators also require ViennaRNA Python bindings for
MFE scoring. The CDS compact example disables MFE scoring by default with
`--mfe_weight 0` so it can run in environments without ViennaRNA.
