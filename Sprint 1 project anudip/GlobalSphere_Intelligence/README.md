# GlobalSphere Intelligence
Advanced Global Population Analytics & Decision Intelligence Platform

Pipeline: World Bank data → Python/Pandas → EDA → MySQL → Power BI.

## Data note
`data/population_demo.csv` is synthetic starter data for testing only, NOT official statistics.
Run the fetch script before using findings in your report.

## Setup (Windows PowerShell)
```powershell
cd path\to\GlobalSphere_Intelligence
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
1. Fetch official World Bank data (2015–2024):
```powershell
python scripts\01_fetch_clean.py
```
2. Generate Matplotlib/Seaborn charts:
```powershell
python scripts\02_eda_visuals.py
```
3. Optional MySQL: copy `.env.example` to `.env`, add your credentials, then:
```powershell
python scripts\03_load_mysql.py
```
4. Build interactive colourful HTML dashboard:
```powershell
python scripts\04_build_dashboard.py
```
Open `outputs\GlobalSphere_Dashboard.html` in Edge or Chrome.

## Create the actual Power BI PBIX
A valid `.pbix` must be authored and saved in Power BI Desktop; this package does
not fabricate an invalid PBIX. In Power BI Desktop: Get Data → Text/CSV →
`data/global_population_clean.csv` → Load. Create measures from
`powerbi/DAX_Measures.txt`, build the visual layout described there, then
File → Save As → `GlobalSphere_Intelligence.pbix`.

Official source: https://data.worldbank.org/indicator/SP.POP.TOTL
