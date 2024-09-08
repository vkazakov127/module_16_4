# -*- coding: utf-8 -*-
# module_16_4.py
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str = None
    age: int = None


@app.get("/users")
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=1, max_length=20,
                                                 description='Enter user name', example='UrbanUser')],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> User:
    # Вычисление атрибута "id" для нового объекта "User"
    if len(users) == 0:
        new_user_id = 1
    else:
        # Сначала сделаем из списка 'users' свой словарь. {'id':index}
        dict1 = {dict_i.id: users.index(dict_i) for dict_i in users}
        new_user_id = max(dict1) + 1
    # Новый объект "User"
    new_user = User(id=new_user_id, username=username, age=age)
    # Добавляем в список "users" объект "new_user"
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=150, description='Enter user ID', example=1)],
        username: Annotated[str, Path(min_length=1, max_length=20,
                                      description='Enter user name', example='UrbanProfi')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=28)]) -> str:
    # Получаем объект "User" из списка "users"
    # Сначала сделаем из списка 'users' свой словарь. {'id':index}
    dict1 = {dict_i.id: users.index(dict_i) for dict_i in users}
    try:
        user_index = dict1[user_id]  # Поиск по ключу в словаре 'dict1'
        user_for_update = users[user_index]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User №{user_id} was not found")
    else:
        # Изменяем объект "User"
        user_for_update.username = username
        user_for_update.age = age
        # Обновляем элемент списка "users"
        # users[user_index] = user_for_update
        return (f"User №{user_id} is updated: "
                f"username={users[user_index].username}, "
                f"age={users[user_index].age}")


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=150, description='Enter user ID', example=2)]) -> str:
    # Сначала сделаем из списка 'users' свой словарь. {'id':index}
    dict1 = {dict_i.id: users.index(dict_i) for dict_i in users}
    try:
        user_index = dict1[user_id]  # Поиск по ключу в словаре 'dict1'
        # Для красоты запомним
        deleted_user_name = users[user_index].username
        deleted_user_age = users[user_index].age
        # Удаляем из списка
        users.pop(user_index)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User №{user_id} was not found")
    else:
        return (f"User №{user_id} is deleted: "
                f"username={deleted_user_name}, "
                f"age={deleted_user_age}")
