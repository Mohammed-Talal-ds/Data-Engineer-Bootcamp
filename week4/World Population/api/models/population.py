from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PopulationRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    country: str = Field(alias="Country")
    population_2026: int = Field(alias="Population 2026")
    yearly_change: Optional[float] = Field(default=None, alias="Yearly Change")
    net_change: Optional[int] = Field(default=None, alias="Net Change")
    density_per_km2: Optional[float] = Field(default=None, alias="Density (P/KmÂ²)")
    land_area_km2: Optional[float] = Field(default=None, alias="Land Area (KmÂ²)")
    migrants_net: Optional[int] = Field(default=None, alias="Migrants (net)")
    fert_rate: Optional[float] = Field(default=None, alias="Fert. Rate")
    median_age: Optional[float] = Field(default=None, alias="Median Age")
    urban_pop_percent: Optional[float] = Field(default=None, alias="Urban Pop %")
    world_share: Optional[float] = Field(default=None, alias="World Share")


class PopulationTotal(BaseModel):
    total_population: int