from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Path
from typing import Annotated
import os
import yaml


from sopros_osa_backend.model import SoprosCountry
from sopros_osa_backend.model import SoprosProvision
from sopros_osa_backend.model import SoprosQuestion
from sopros_osa_backend.model import SoprosRule
from sopros_osa_backend.model import SoprosStatus
from sopros_osa_backend.model import SoprosType


@asynccontextmanager
async def lifespan(app: FastAPI):
    resource_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

    # Load the provisions
    with open(os.path.join(resource_folder, "provision.yml"), "r") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            [sopros_provisions.append(SoprosProvision(**entry)) for entry in yaml_data["provision"]]
        except yaml.YAMLError as exc:
            print(exc)

    # Load the status
    with open(os.path.join(resource_folder, "status.yml"), "r") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            [sopros_status.append(SoprosStatus(**entry)) for entry in yaml_data["status"]]
        except yaml.YAMLError as exc:
            print(exc)

    # Load the types
    with open(os.path.join(resource_folder, "type.yml"), "r") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            [sopros_types.append(SoprosType(**entry)) for entry in yaml_data["type"]]
        except yaml.YAMLError as exc:
            print(exc)

    # Load the countries
    with open(os.path.join(resource_folder, "country.yml"), "r") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            [sopros_countries.append(SoprosCountry(**entry)) for entry in yaml_data["country"]]
        except yaml.YAMLError as exc:
            print(exc)
    yield
    # clean up sopros and release the resources
    sopros.clear()

sopros = {}
sopros_countries: list[SoprosCountry] = []
sopros_provisions: list[SoprosProvision] = []
sopros_status: list[SoprosStatus] = []
sopros_types: list[SoprosType] = []

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/country")
async def read_country(country_id: str) -> SoprosCountry:
    return next(x for x in sopros_countries if x.id == country_id)

@app.get("/provisions")
async def read_provisions() -> list[SoprosProvision]:
    return sopros_provisions

@app.get("/status")
async def read_status() -> list[SoprosStatus]:
    return sopros_status

@app.get("/types")
async def read_types() -> list[SoprosType]:
    return sopros_types

@app.post("/calc")
async def calc(country_id: str, status_ids: list[str]) -> list[SoprosRule]:
    print(status_ids)
    country = next(x for x in sopros_countries if x.id == country_id)
    rules = country.rules
    rules = [x for x in rules if x.status_id in status_ids]
    return rules



# @app.get("/country")
# async def read_country() -> dict[str, SOPROSCountry]:
#     return sopros


# @app.get("/country/{id}")
# async def read_country(
#         id: Annotated[str,
#             Path(description="The ID Country")
#         ]
# ) -> SOPROSCountry:

#     if id not in sopros.keys():
#         raise HTTPException(status_code=404,
#             detail=f"Country key {id} not found. Vaild keys are {[*sopros]}")
#     return sopros[id]



# @app.get("/states/{country_id}")
# async def read_states(
#         country_id: Annotated[str,
#             Path(description="The ID Country")
#         ]
# ) -> list[State]:

#     if country_id not in sopros.keys():
#         raise HTTPException(status_code=404,
#             detail=f"Country key {country_id} not found. Vaild keys are {[*sopros]}")
#     return sopros[country_id].states


