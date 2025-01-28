from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import APIRouter, FastAPI, HTTPException, Path
from fastapi.responses import PlainTextResponse
import shelve
from typing import Annotated
import uuid
import os
import yaml


from sopros_osa_backend.model import SoprosAnswer
from sopros_osa_backend.model import SoprosCountry
from sopros_osa_backend.model import SoprosCountryName
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
    [sopros_country_names.append(SoprosCountryName(**entry)) for entry in yaml_data["country"]]

    # saved date folder
    os.makedirs(os.getenv("SAVE_DIR", "./saved_data"), exist_ok=True)
    yield
    # clean up sopros and release the resources
    sopros.clear()

save_full_pathname = os.path.join(os.getenv("SAVE_DIR", "./saved_data"), "answers")
sopros = {}
sopros_countries: list[SoprosCountry] = []
sopros_country_names: list[SoprosCountryName] = []
sopros_provisions: list[SoprosProvision] = []
sopros_status: list[SoprosStatus] = []
sopros_types: list[SoprosType] = []

app = FastAPI(lifespan=lifespan,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    servers=[{"url":"http://localhost:8000/"}, {"url":"https://abcoden.de/"}])
router = APIRouter(prefix="/api")


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/download/answers/json")
async def download_answers_json() -> list[SoprosAnswer]:
    with shelve.open(save_full_pathname) as db:
        return list(db.values())

@router.get("/download/answers/csv/simple", response_class=PlainTextResponse)
async def download_answers_csv_simple() -> str:
    result = ""
    with shelve.open(save_full_pathname) as db:
        for answer in db.values():
            result += f"{answer.id};{answer.country};{answer.created}\n"
    return  result

@router.get("/download/answers/csv/full", response_class=PlainTextResponse)
async def download_answers_csv_full() -> str:
    result = ""
    all_status_ids = set()
    all_rule_ids = set()
    for country in sopros_countries:
        for question in country.questions:
            all_status_ids.add(question.status_id)
        for question in country.questions_athlete:
            all_status_ids.add(question.status_id)
        for rule in country.rules:
            all_rule_ids.add(rule.id)
    all_status_ids = sorted(all_status_ids)
    all_rule_ids = sorted(all_rule_ids)
    header = ["id", "country", "created"]
    header.extend(all_status_ids)
    header.extend(all_rule_ids)
    result += ';'.join(header) + '\n'
    with shelve.open(save_full_pathname) as db:
        for answer in db.values():
            row = [answer.id, answer.country, str(answer.created)]
            for status in all_status_ids:
                row.extend(['x' if status in answer.status_ids else ''])
            for rule in all_rule_ids:
                row.extend(['x' if rule in answer.provision_ids else ''])
            result += ';'.join(row) + '\n'
    return result

@router.get("/answer/{answer_id}")
async def read_answer(answer_id: str) -> SoprosAnswer:
    print(save_full_pathname)
    with shelve.open(save_full_pathname) as db:
        return db[answer_id]

@router.post("/answer")
async def calc(country_id: str, status_ids: list[str]) -> SoprosAnswer:
    rules = calc_provisions(country_id, status_ids)
    answer = SoprosAnswer()
    answer.id = str(uuid.uuid4())
    answer.country = country_id
    answer.created = datetime.now()
    answer.status_ids = status_ids
    answer.provision_ids = [x.id for x in rules]
    save_answer(answer)
    return answer


@router.get("/countries")
async def read_country() -> list[SoprosCountryName]:
    return sopros_country_names

@router.get("/country/{country_id}")
async def read_country(country_id: str) -> SoprosCountry:
    return next(x for x in sopros_countries if x.id == country_id)

@router.get("/provisions")
async def read_provisions() -> list[SoprosProvision]:
    return sopros_provisions

@router.get("/status")
async def read_status() -> list[SoprosStatus]:
    return sopros_status

@router.get("/types")
async def read_types() -> list[SoprosType]:
    return sopros_types

@router.post("/calc/{country_id}")
async def calc(country_id: str, status_ids: list[str]) -> list[SoprosRule]:
    return calc_provisions(country_id, status_ids)

def calc_provisions(country_id: str, status_ids: list[str]) -> list[SoprosRule]:
    country = next(x for x in sopros_countries if x.id == country_id)
    rules = country.rules
    rules = [x for x in rules if x.status_id in status_ids]
    all_invalidate_ids = [x for rule in rules for x in rule.invalidates_rule_ids]
    rules = [x for x in rules if x.id not in all_invalidate_ids]
    return rules

def save_answer(answer: SoprosAnswer):
    with shelve.open(save_full_pathname) as db:
        db[answer.id] = answer
    print(str(answer))



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

app.include_router(router)
