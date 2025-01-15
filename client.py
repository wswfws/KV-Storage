import asyncio
import hashlib

from aiogram.client.session import aiohttp
from aiohttp import ClientResponse

server_adrrs = ["http://localhost:8000", "http://localhost:8001"]

user = {
    "user_id": "1",
    "password_hash": hashlib.sha256("password".encode()).hexdigest()
}


async def add_value(key, value):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for server_adrr in server_adrrs:
            json = {"key": key, "value": value, "user": user, "finish_value": True}
            task = asyncio.create_task(session.post(server_adrr + "/add_value", json=json))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                return False
            elif result.status != 200:
                return False
    return True


async def add_value_part(key, value) -> (bool,):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for server_adrr in server_adrrs:
            json = {"key": key, "value": value, "user": user, "finish_value": False, }
            task = asyncio.create_task(session.post(server_adrr + "/add_value", json=json))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                return False
            elif result.status != 200:
                return False
    return True


async def sync_values(servers, key, values):
    for value in values:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for server_adrr in servers:
                json = {"key": key, "user": user}
                task = asyncio.create_task(session.post(server_adrr + "/clear_key", json=json))
                tasks.append(task)
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    return False
                elif result.status != 200:
                    return False
            tasks = []
            for server_adrr in servers:
                json = {"key": key, "value": value, "user": user, "finish_value": True}
                task = asyncio.create_task(session.post(server_adrr + "/add_value", json=json))
                tasks.append(task)
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    return False
                elif result.status != 200:
                    return False
    return True


async def get_value(key) -> (bool, str,):
    values = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for server_adrr in server_adrrs:
            json = {"key": key, "user": user}
            task = asyncio.create_task(session.post(server_adrr + "/get_value", json=json))
            tasks.append(task)
        results: list[ClientResponse] = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                return False
            elif result.status != 200:
                return False
            values.append((result.url, (await result.json())["value"]))

    main_server = server_adrrs[0]
    correct_value = values[0][0]

    for val in values:
        if main_server in str(val[0]):
            correct_value = val[1]

    await sync_values([str(val[0].parent) for val in values if val[1] != correct_value], key, correct_value)

    return correct_value


async def clear_key(key) -> (bool,):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for server_adrr in server_adrrs:
            json = {"key": key, "user": user}
            task = asyncio.create_task(session.post(server_adrr + "/clear_key", json=json))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                return False
            elif result.status != 200:
                return False
    return True


async def main():
    print(await clear_key("key"))  # True
    print(await add_value("key", "value1"))  # True
    print(await get_value("key"))  # ['value1']
    print(await add_value("key", "value2"))  # True
    print(await get_value("key"))  # ['value1', 'value2']
    print(await add_value("key", "value3"))  # True
    print(await get_value("key"))  # ['value1', 'value2', 'value3']

    # part value
    print(await clear_key("key"))  # True
    print(await get_value("key"))  # []
    print(await add_value_part("key", "valu"))  # True
    print(await get_value("key"))  # []
    print(await add_value("key", "eFull"))  # True
    print(await get_value("key"))  # ['valueFull']

    print(f"{'sync_data':_^30}")
    print(await clear_key("key"))  # True
    global server_adrrs
    _servers = server_adrrs.copy()
    server_adrrs = [server_adrrs[0]]
    print(await add_value("key", "value"))  # True
    server_adrrs = _servers
    print(await get_value("key"))  # ["value"]


if __name__ == '__main__':
    asyncio.run(main())
