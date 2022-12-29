import json
from fastapi import FastAPI, Request, Depends, Form, status, APIRouter
from models import db, Todo
from utils import createResponse, createNotFoundResponse
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

todoRouter = APIRouter(
    prefix="/todo",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={
        404: {"description": "Not found"}
        },
)

@app.middleware("http")
async def openAndCloseDb(request: Request, call_next):
    db.connect(reuse_if_open=True)
    response = await call_next(request)
    db.close()
    return response

@todoRouter.get("/")
async def home(request: Request):
    todos = Todo.select()
    items = dict()
    for todo in todos:
        items[todo.id] = todo.toJson()
    result = createResponse(items)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

@todoRouter.post("/")
async def add(request: Request, task: str = Form(...)):
    todo = Todo()
    todo.task= task
    todo.save()
    result = createResponse(todo.toJson())
    return JSONResponse(result, status_code=status.HTTP_201_CREATED)

@todoRouter.get("/{todo_id}")
async def getItem(request: Request, todo_id: int):
    todo = Todo.get_or_none(todo_id)
    print(todo)
    if (todo is None):
        return JSONResponse(createNotFoundResponse(), status_code=status.HTTP_404_NOT_FOUND)
    result = createResponse(todo.toJson())
    return JSONResponse(result)

@todoRouter.patch("/{todo_id}")
async def add(request: Request, todo_id: int, task: str = Form(None), completed: bool = Form(False)):
    todo = Todo.get_or_none(todo_id)
    if (todo is None):
        return JSONResponse(createNotFoundResponse(), status_code=status.HTTP_404_NOT_FOUND)
    if(task is not None):
        todo.task = task
    todo.completed = completed
    todo.save()
    result = createResponse(todo.toJson())
    return JSONResponse(result)

@todoRouter.delete("/{todo_id}")
async def delete(request: Request, todo_id: int):
    todo = Todo.get_or_none(todo_id)
    if (todo is None):
        return JSONResponse(createNotFoundResponse(), status_code=status.HTTP_404_NOT_FOUND)
    todo.delete_instance()
    return JSONResponse(createResponse(None))


app.include_router(todoRouter)