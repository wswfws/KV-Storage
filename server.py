import sys
from collections import defaultdict

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from Models.User import UserModel, convert_user_model_to_user, User
from config import ServerConfig
from storage.FileBasedKeyValueStore import FileBasedKeyValueStore

app = FastAPI()


class AddValueRequestBody(BaseModel):
    key: str
    value: str
    finish_value: bool
    user: UserModel


# Глобальный буфер для промежуточных значений
buffer_store = defaultdict(str)


def checkUser(user: User):
    if not any(acs_user["user_id"] == user.user_id and acs_user["password_hash"] == user.password_hash
               for acs_user in ServerConfig.ACSEPT_USERS):
        raise HTTPException(status_code=401, detail="Invalid user_id or password")


@app.post("/add_value")
def add_value(body: AddValueRequestBody):
    user = convert_user_model_to_user(body.user)
    checkUser(user)
    store = FileBasedKeyValueStore(user.get_user_filename())

    buffer_key = f"{user.get_user_filename()}:{body.key}"

    if body.finish_value:
        final_value = buffer_store[buffer_key] + body.value
        store.add(body.key, final_value)
        buffer_store.pop(buffer_key, None)
        return {"status": "OK"}
    else:
        buffer_store[buffer_key] += body.value
        return {"status": "IN_PROGRESS"}


class GetValueRequestBody(BaseModel):
    key: str
    user: UserModel


@app.post("/get_value")
def get_value(body: GetValueRequestBody):
    user = convert_user_model_to_user(body.user)
    checkUser(user)
    store = FileBasedKeyValueStore(user.get_user_filename())
    value = store.get(body.key)
    return {"key": body.key, "value": value}


class ClearKeyRequestBody(BaseModel):
    key: str
    user: UserModel


@app.post("/clear_key")
def clear_key(body: ClearKeyRequestBody):
    user = convert_user_model_to_user(body.user)
    checkUser(user)
    store = FileBasedKeyValueStore(user.get_user_filename())
    store.delete(body.key)
    return {"status": "OK"}


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

    if port != 8000:
        ServerConfig.STORAGE_PATH += f"{port}\\"

    uvicorn.run(app, host="localhost", port=port)
