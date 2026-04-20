from fastapi import FastAPI

from api.routes.population import router as population_router


app = FastAPI(title="World Population API", version="1.0.0")


@app.get("/")
def root() -> dict:
    return {
        "message": "World Population API",
        "endpoints": ["/population", "/top10", "/population-sum"],
    }


app.include_router(population_router)