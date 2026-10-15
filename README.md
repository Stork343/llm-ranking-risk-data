# Data for semantic ranking and predictive risk control

This repository provides the curated LendingClub input, the UCI credit card input and recorded language-model rankings used in the variable-selection studies. The archive preserves the relative paths expected by the analysis programs.

## Obtain the inputs

Download [inputs-v1.zip from the tagged release](https://github.com/Stork343/llm-ranking-risk-data/releases/download/v1.0.0/inputs-v1.zip) or restore its contents with Python and a configured GitHub CLI:

```bash
python fetch_data.py --output-root ../analysis
```

The destination contains sibling `JBES` and `SSM` directories. Extract the analysis code package into the same destination. The download script verifies the archive size and ZIP integrity and checks existing files before extracting missing files.

The tagged version is `v1.0.0`. `manifest.json` lists every archived path and its size.

The original training identifiers accompany the curated loan input so that the programs can restore the same training sample. To prepare the original loan matrices after extracting the analysis code, run `python3 SSM/experiments/risk_loan.py prepare` from the analysis directory.

## Recorded rankings

The observations include 2,048 valid heating-task responses, 64 loan-task responses, 256 new 64-field responses and 256 credit-card responses. Original requests and sampling protocols accompany the responses. The 16-field dimension-study snapshots reuse the first eight heating-task responses from each sequence and are retained at the paths expected by the programs.

## Sources and attribution

The curated LendingClub data are version 0.1 of *Lending Club loan dataset for granting models*, by Miller Janny Ariza-Garzon, Mario Sanz-Guerrero, Javier Arroyo Gallardo and Lending Club, 2024. Source: [Zenodo record](https://zenodo.org/records/11295916), DOI [10.5281/zenodo.11295916](https://doi.org/10.5281/zenodo.11295916). The file is compressed without changing its contents and retains the source's CC BY 4.0 license.

*Default of Credit Card Clients* is attributed to I-Cheng Yeh, 2009. Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/350/default%2Bof%2Bcredit%2Bcard%2Bclients), DOI [10.24432/C55S3H](https://doi.org/10.24432/C55S3H). The original archive and Excel file retain CC BY 4.0. The accompanying analysis CSV records the same observations in CSV form.

The source licenses apply to their respective datasets. The remaining observations are recorded model requests and outputs collected for the studies.

## Later loan cohorts

The 2019 and 2020 loan inputs use Kaggle version 3, dated December 15, 2020, and the September 2022 LendingClub quarterly outcome files. `manifest.json` gives the original source URLs and filenames. Obtain those archives from their original sources and use the source-processing programs supplied with the analysis code. The Kaggle metadata lists its license as “Other”; the quarterly archives have no separate redistribution grant identified in the available source information.

The code package provides `download_kaggle_archive.py`, `build_paired_loan_updates.py` and `lendingclub_snapshot_alignment.py` for this preparation. The original sources and their terms govern those archives.
