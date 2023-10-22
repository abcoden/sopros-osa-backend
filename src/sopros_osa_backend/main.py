from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Path
from typing import Annotated
import os
import yaml


from sopros_osa_backend.model import State
from sopros_osa_backend.model import SOPROSCountry


@asynccontextmanager
async def lifespan(app: FastAPI):
    resource_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    for file in os.scandir(resource_folder):
        filename_split = file.name.split('.')
        # check filenames in folder
        if (len(filename_split) != 2 or filename_split[1] not in ["yml", "yaml"]):
            continue
        # Load the sorpos country config
        with open(file.path, "r") as stream:
            try:
                yaml_data = yaml.safe_load(stream)
                sopros[filename_split[0]] = SOPROSCountry(**yaml_data)
            except yaml.YAMLError as exc:
                print(exc)
    yield
    # clean up sopros and release the resources
    sopros.clear()

sopros = {}

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/country")
async def read_country() -> dict[str, SOPROSCountry]:
    return sopros


@app.get("/country/{id}")
async def read_country(
        id: Annotated[str,
            Path(description="The ID Country")
        ]
) -> SOPROSCountry:
    return sopros[id]



@app.get("/states/{country_id}")
async def read_states(
        country_id: Annotated[str,
            Path(description="The ID Country")
        ]
) -> list[State]:

    if country_id not in sopros.keys():
        raise HTTPException(status_code=404,
            detail=f"Country key {country_id} not found. Vaild keys are {[*sopros]}")
    return sopros[country_id].states


