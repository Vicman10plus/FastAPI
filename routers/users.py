from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator

router = APIRouter()


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    @validator('id')
    def id_must_be_positive(self, value):
        if value < 0:
            raise ValueError('Id must be a positive value')
        return value

    @validator('name')
    def name_must_not_be_empty(self, value):
        if not value.strip():
            raise ValueError('Name must not be empty')
        return value

    @validator('surname')
    def surname_must_not_be_empty(self, value):
        if not value.strip():
            raise ValueError('Surname must not be empty')
        return value

    @validator('age')
    def age_must_be_positive(self, value):
        if value < 0:
            raise ValueError('Age must be a positive value')
        return value


users_list = [User(id=1, name="Juan", surname="Perez", age=35),
              User(id=2, name="Pedro", surname="Ramirez", age=35),
              User(id=3, name="Jose", surname="Alvarez", age=33)]


@router.get("/users")
async def users():
    return users_list


@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


@router.get("/user/")
async def user(id: int):
    return search_user(id)


@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="User already exists")

    users_list.append(user)
    return user.id


@router.put("/user/")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "User has not been updated"}

    return {"message": f"User {user.name} has been updated"}


@router.delete("/user/{id}")
async def user(id: int):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "User has not been deleted"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User has not been found"}
