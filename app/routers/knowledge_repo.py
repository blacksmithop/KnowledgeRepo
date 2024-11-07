from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app import Category, AddCategory, DeleteCategory, MongoDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")

mongo = MongoDB()


@router.get("/")
async def index(request: Request):
    dataset = mongo.get_domain_knowledge()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"data": dataset}
    )


@router.get("/list_category", tags=["Knowledge"])
async def load_data(request: Request):
    dataset = mongo.get_domain_knowledge()
    return dataset

@router.post("/search_by_category", tags=["Knowledge"])
async def load_data(request: Request):
    dataset = mongo.get_domain_knowledge()
    return dataset


@router.post("/add_category", tags=["Knowledge"])
async def add_category(payload: AddCategory):
    print(f"Received payload for category {payload.name}")
    mongo.add_category(data=payload)
    return 200


@router.delete("/delete_category", tags=["Knowledge"])
async def dlete_category(payload: DeleteCategory):
    print(f"Deleting category {payload.id}")
    mongo.delete_category(category_id=payload.id)
    return 200
