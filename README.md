## FITS file processer

Convert light (source images) to aligned frames.

Fundamentals of Observational Astronomy (基礎天文觀測)

## Directory Structure
```
Repo
├── align.py
├── merge.py
├── requirements.txt
│
├── bias/
│   ├── Bias-20230310@213102-000S.fts
│   └── * Will be broken if bin2 files exists
├── dark/
│   └── 300s/
│       └── Dark-20230310@214015-300S.fts
├── flat/
│   ├── 20230310/
│   │   ├── B/
│   │   │   └── AutoFlat-20230310@102526-B_319144-Bin1-001.fts
│   │   ├── V/
│   │   ├── R/
│   │   └── Ha/
│   └── 20230311/
│
├── light/
│   ├── 20230310-NGC3338-001B300s.fits
│   ├── 20230310-NGC3338-001R300s.fits
│   ├── 20230310-NGC3338-001V300s.fits
│   ├── 20230310-NGC3338-002B300s.fits
│   └── * Files from Lulin, only bin1 supported
│
├── calibrated/
│   ├── NGC3338-20230310-B-300s-001.fits
│   └── * Processed with corresponding (dark, flat)
├── normalized/
│   ├── NGC3338-20230310-B-300s-001.fits
│   └── * Adjust brightness for every (target, date)
│── aligned/
│   ├── NGC3338-20230310-B-300s-001.fits
│   └── * Align frame for every (target, date)
│
└── merged/
    ├── NGC3338-20230310-B.fits
    ├── NGC3338-20230310-R.fits
    ├── NGC3338-20230310-V.fits
    ├── NGC3338-20230310-preview.png
    └── * Final artifact
```

## Usage

```bash
mkdir calibrated/ normalized/ aligned/ merged/
pip3 install -r requirements.txt
python3 align.py
python3 merge.py
```

## Contact

Sean Wei (<https://sean.cat/about>)
