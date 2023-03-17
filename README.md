# 111B 基礎天文觀測

Fundamentals of Observational Astronomy

## FITS file processer

Convert light (source images) to aligned frames.

## Directory Structure
```
Repo
├── main.py  * program file
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
│   └── 20230311
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
└── aligned/
    ├── NGC3338-20230310-B-300s-001.fits
    └── * Align frame for every (target, date)
```

## Usage

```bash
mkdir calibrated/ normalized/ aligned/
pip3 install -r requirements.txt
python3 main.py
```

## Contact

Sean Wei (<https://sean.cat/about>)
