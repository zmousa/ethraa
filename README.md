# Arabicthon
- https://arabicthon.ksaa.gov.sa

## Team
- فريق الإثراء الرقمي



## Setup Dev Environment (Mac)
```
brew install --cask miniforge
brew install pipx
conda create -n arabicthon python=3.10

conda activate arabicthon
pip install "poetry<1.2"

poetry lock
poetry install
```

## Run locally
```
streamlit run --server.enableCORS false --browser.gatherUsageStats false app/app.p
```
