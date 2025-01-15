import pytest

from client import clear_key, add_value, get_value

"""
python server.py 8000
python server.py 8001
"""


class TestClient:

    @pytest.fixture(autouse=True)
    @pytest.mark.asyncio
    async def setup_method(self):
        """Clear the storage before each test."""
        assert await clear_key("key")

    @pytest.mark.asyncio
    async def test_add_value(self):
        assert await add_value("key", "value1")
        assert (await get_value("key")) == ['value1']
        assert await add_value("key", "value2")
        assert (await get_value("key")) == ['value1', 'value2']
        assert await add_value("key", "value3")
        assert (await get_value("key")) == ['value1', 'value2', 'value3']

    @pytest.mark.asyncio
    async def test_add_value(self):
        assert await add_value("key", "value1")
        assert (await get_value("key")) == ['value1']
        assert await add_value("key", "value2")
        assert (await get_value("key")) == ['value1', 'value2']
        assert await add_value("key", "value3")
        assert (await get_value("key")) == ['value1', 'value2', 'value3']
