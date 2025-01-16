import hashlib

import pytest

from client import clear_key, add_value, get_value, add_value_part
from config import ClientConfig

"""
python server.py 8000
python server.py 8001
"""


class TestClient:

    async def setup_function(self):
        """Clear the storage before each test."""
        await clear_key("key")

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_add_value(self):
        await self.setup_function()
        assert await add_value("key", "value1")
        assert (await get_value("key")) == ['value1']
        assert await add_value("key", "value2")
        assert (await get_value("key")) == ['value1', 'value2']
        assert await add_value("key", "value3")
        assert (await get_value("key")) == ['value1', 'value2', 'value3']

    @pytest.mark.dependency(depends=["test_add_value"])
    @pytest.mark.asyncio
    async def test_add_value_part(self):
        await self.setup_function()
        assert await add_value_part("key", "valu")
        assert (await get_value("key")) == []
        assert await add_value("key", "eFull")
        assert (await get_value("key")) == ['valueFull']

    @pytest.mark.dependency(depends=["test_add_value_part"])
    @pytest.mark.asyncio
    async def test_sync_server_data(self):
        await self.setup_function()
        _servers = ClientConfig.SERVER_ADRRS.copy()
        ClientConfig.SERVER_ADRRS = [ClientConfig.SERVER_ADRRS[0]]
        assert await add_value("key", "value")
        ClientConfig.SERVER_ADRRS = _servers
        assert (await get_value("key")) == ["value"]

    @pytest.mark.asyncio
    async def test_users(self):
        await self.setup_function()
        assert await add_value("key", "user1")
        user = ClientConfig.USER.copy()
        ClientConfig.USER = {
            "user_id": "2",
            "password_hash": hashlib.sha256("password2".encode()).hexdigest()
        }
        assert await add_value("key", "user2")
        assert (await get_value("key")) == ["user2"]
        ClientConfig.USER = user
        assert (await get_value("key")) == ["user1"]
