# Installation

Clone the repository with Git LFS enabled so the released generation checkpoints are downloaded correctly:

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

Or install the core pip dependencies:

```bash
pip install --extra-index-url https://download.pytorch.org/whl/cu118 -r requirements.txt
```

Check that the package imports correctly:

```bash
python scripts/quick_import_check.py
```

## Checkpoints

The released generation checkpoints are tracked with Git LFS:

```text
generation/
├── 5utr/Model.pth
├── cds/Model.pth
└── 3utr/Model.pth
```

Verify checkpoint integrity:

```bash
shasum -a 256 -c MODEL_CHECKSUMS.sha256
```

If Git LFS is not installed, these paths may contain small pointer files instead of the real checkpoints.

## Full data and model archive

The full mROSE data and model archive is available on Zenodo:

- DOI: [10.5281/zenodo.20756460](https://doi.org/10.5281/zenodo.20756460)

For full-scale experiments, download the Zenodo archive and place large datasets outside normal Git history, for example under `data/raw/`. The repository examples remain intentionally small so they can document file formats and command-line usage.
