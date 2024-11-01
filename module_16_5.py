from fastapi import FastAPI, Path, HTTPException, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel

from fastapi.templating import Jinja2Templates

new_app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@new_app.get("/")
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@new_app.get("/users/{user_id}")
def get_user_by_id(request: Request, user_id: int = Path(ge=1, description='User ID')) -> HTMLResponse:
    try:
        user = next(user for user in users if user.id == user_id)
    except:
        raise HTTPException(status_code=404, detail=f'User with ID {user_id} not found.')

    return templates.TemplateResponse('users.html', {'request': request, 'user': user})


@new_app.post('/user/{username}/{age}')
async def post_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: int = Path(ge=18, le=120, description='Enter age', example=24)
) -> str:
    id = 1
    id_list = [user.id for user in users]
    if id not in id_list:
        user = User(id=1, username=username, age=age)
        users.append(user)
    else:
        while id in id_list:
            id += 1
        user = User(id=id, username=username, age=age)
        users.append(user)
    return f"User {username} is registered"


@new_app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail="User was not found")


@new_app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]) -> User:
    for i in range(len(users)):
        if users[i].id == user_id:
            return users.pop(i)
    else:
        raise HTTPException(status_code=404, detail='User was not found')


@new_app.get("/users")
async def get_users() -> list[User]:
    return users
