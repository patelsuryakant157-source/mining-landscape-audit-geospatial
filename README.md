\# Spatiotemporal Audit of Surface Coal Extraction, Landscape Fragmentation, and Riparian Encroachment (2001–2024)



\[!\[Earth Engine](https://img.shields.io/badge/Google%20Earth%20Engine-API-green)](https://earthengine.google.com/)

\[!\[PyLandStats](https://img.shields.io/badge/PyLandStats-Landscape%20Metrics-blue)](https://pylandstats.readthedocs.io/)

\[!\[Accuracy](https://img.shields.io/badge/Overall%20Accuracy-88.33%25-brightgreen)]()

\[!\[Kappa](https://img.shields.io/badge/Kappa%20(κ)-0.8444-orange)]()



An empirical, multi-decadal remote sensing and landscape ecology audit of the \*\*Dhanpuri–Amlai Coalfield Complex\*\* (Shahdol District, Madhya Pradesh, Central India).



This repository implements a reproducible Python and Google Earth Engine pipeline to track 23-year surface mining dynamics, patch-level forest fragmentation, and riparian buffer encroachment along the Son River using \*\*Landsat 7 ETM+\*\*, \*\*Landsat 8 OLI\*\*, and \*\*FRAGSTATS-compliant landscape metrics\*\*.



\---



\## Key Empirical Findings (2001 vs. 2024)



\* \*\*Mining Footprint Consolidation:\*\* Active surface mining contracted from \*\*1,924.38 ha\*\* (8.59% of landscape across 1,799 patches) in 2001 to a consolidated core pit of \*\*269.46 ha\*\* (1.20% across 279 patches) in 2024. Edge density dropped from \*\*38.94 m/ha to 5.63 m/ha\*\*.

\* \*\*Canopy Recovery on Legacy Overburden:\*\* Core forest canopy expanded five-fold from \*\*2,303.01 ha\*\* (10.28%) to \*\*11,664.18 ha\*\* (52.08%). Mean Forest Patch Size increased from \*\*1.51 ha to 9.44 ha\*\*, driven by biological reclamation over decommissioned overburden dumps.

\* \*\*Riparian Buffer De-escalation:\*\* Active mining exposure inside the \*\*1 km critical riparian buffer\*\* of the Son River dropped by \*\*71.26%\*\* (-214.56 ha, from 301.08 ha to 86.51 ha), though 86.51 ha remains within this primary discharge zone.

\* \*\*Statistical Validation:\*\* Stratified random validation ($N = 240$ points) verified \*\*88.33% Overall Classification Accuracy\*\* ($\\kappa = 0.8444$), with a \*\*100.00% User's Accuracy\*\* for active mining surfaces.



\---



\## Visual Summary



\### Calibrated Landscape Classification (2001 vs. 2024)

!\[Landscape Classification](figures/dhanpuri\_calibrated\_comparison.png)



\### Son River Multi-Ring Riparian Buffer Audit (1 km, 2 km, 5 km)

!\[Riparian Buffers](figures/son\_river\_buffer\_audit.png)



\---



\## Methodology Highlights



1\. \*\*Dry-Soil vs. Coal Spectral Calibration:\*\* Combines NDVI and MNDWI with a Shortwave Infrared ($\\rho\_{\\text{SWIR1}} < 0.20$) and Visible Red ($\\rho\_{\\text{Red}} < 0.15$) brightness filter to eliminate false positives from bare post-harvest agricultural fields and dry river sands.

2\. \*\*Landscape Fragmentation (`PyLandStats`):\*\* Computes Class Area ($CA$), Percentage of Landscape ($PLAND$), Number of Patches ($NP$), Mean Patch Size ($AREA\\\_MN$), and Edge Density ($ED$) using 8-neighbor connectivity.

3\. \*\*Riparian Encroachment Modeling:\*\* Uses Euclidean distance transformations to quantify active extraction inside 1 km, 2 km, and 5 km buffers along the Son River.

4\. \*\*Interactive Web Dashboard (`app.py`):\*\* Built with Streamlit and Plotly to explore maps, metrics, and validation matrices interactively.



\---



\## Repository Structure



```text

├── app.py                              # Interactive Streamlit web dashboard

├── requirements.txt                    # Python environment dependencies

├── README.md                           # Project documentation

├── data/

│   ├── dhanpuri\_calibrated\_2001.tif    # Calibrated 4-class GeoTIFF (2001)

│   ├── dhanpuri\_calibrated\_2024.tif    # Calibrated 4-class GeoTIFF (2024)

│   ├── dhanpuri\_fragmentation\_audit.csv# PyLandStats structural metrics

│   ├── son\_river\_encroachment\_audit.csv# Riparian buffer distance audit

│   ├── dhanpuri\_confusion\_matrix.csv   # Error contingency matrix

│   └── dhanpuri\_accuracy\_metrics.csv   # Class-wise Producer's/User's accuracy

├── figures/

│   ├── dhanpuri\_calibrated\_comparison.png

│   └── son\_river\_buffer\_audit.png

├── outputs/

│   └── Dhanpuri\_Amlai\_Ecological\_Audit\_Manuscript.pdf

└── scripts/

&#x20;   ├── day4\_calibrated\_export.py

&#x20;   ├── day5\_fragmentation\_audit.py

&#x20;   ├── day8\_buffer\_audit.py

&#x20;   ├── day9\_accuracy\_assessment.py

&#x20;   └── generate\_manuscript\_pdf.py

