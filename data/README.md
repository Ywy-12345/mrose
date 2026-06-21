# Data organization

Large training datasets are not committed to this GitHub-ready package. The full mROSE data and model archive is available on Zenodo at [10.5281/zenodo.20756460](https://doi.org/10.5281/zenodo.20756460).

Task-specific miniature examples are stored inside each experiment folder so the expected input schema is visible next to the corresponding script:

```text
experiments/5utr_mrl/example/
experiments/cds_degradation/example/
experiments/3utr_rbp/example/
experiments/full_length_stability/example/
```

For full-scale training, download the Zenodo archive and place large datasets outside Git, for example under `data/raw/`. See `DATA_MANIFEST.md` for source-style dataset descriptions.
