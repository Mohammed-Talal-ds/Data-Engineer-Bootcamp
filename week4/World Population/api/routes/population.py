from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

from api.models.population import PopulationRecord, PopulationTotal


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent.parent / "data" / "cleaned_data.csv"


def get_population_data() -> pd.DataFrame:
    if not CSV_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Data file not found: {CSV_PATH}")

    return pd.read_csv(CSV_PATH)


@router.get("/population", response_model=list[PopulationRecord])
def population_data() -> list[dict]:
    dataframe = get_population_data().sort_values("Population 2026", ascending=False)
    return dataframe.to_dict(orient="records")


@router.get("/top10", response_model=list[PopulationRecord])
def top_10_population() -> list[dict]:
    dataframe = get_population_data().sort_values("Population 2026", ascending=False).head(10)
    return dataframe.to_dict(orient="records")


@router.get("/population-sum", response_model=PopulationTotal)
def population_sum() -> dict:
    dataframe = get_population_data()
    total_population = int(dataframe["Population 2026"].sum())

    return {"total_population": total_population}