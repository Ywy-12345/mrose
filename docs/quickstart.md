# Quick start

This page gives the shortest path from a fresh checkout to a working mROSE
generation run. Use it first, then move to the detailed pages for each workflow.

## 1. Choose an entry point

| Goal | Start here |
|---|---|
| Try mROSE in a browser | [Web server](web_server.md) |
| Run local generation examples | [Sequence generation](generation.md) |
| Follow a notebook with displayed results | [Generation notebook](notebooks/mROSE_generation.ipynb) |
| Reproduce compact training examples | [Experiments](experiments.md) |
| Understand repository layout | [Project structure](PROJECT_STRUCTURE.md) |

## 2. Install and check the environment

Clone with Git LFS so the released generation checkpoints are downloaded:

```bash
git lfs install
git clone https://github.com/Ywy-12345/mrose.git
cd mrose
git lfs pull
```

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate mROSE
```

Then run the import check:

```bash
python scripts/quick_import_check.py
```

## 3. Run the smallest generation example

Print dependency and checkpoint status:

```bash
python scripts/generate_sequences.py
```

Run one compact example:

```bash
python scripts/generate_sequences.py --run 5utr
```

Useful alternatives:

```bash
python scripts/generate_sequences.py --run cds
python scripts/generate_sequences.py --run 3utr
python scripts/generate_sequences.py --run full_length
python scripts/generate_sequences.py --run all
```

Generated CSV and FASTA outputs are written under `outputs/generation/`.

## 4. Read the output

The most useful files are the `top` CSV files. They contain ranked candidate
sequences plus region-specific scores and sequence features.

For full-length mRNA generation, the output table also includes the generated
5′ UTR, CDS and 3′ UTR components used to assemble each full transcript.

## 5. Next steps

- Use [Sequence generation](generation.md) for direct commands and full-length
  assembly details.
- Use [Web server](web_server.md) for browser access and API examples.
- Use [Experiments](experiments.md) for compact training and prediction examples.
