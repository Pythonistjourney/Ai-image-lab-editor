import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_colorize(client: AsyncClient):
    # TODO: Mock upload and service
    response = await client.post("/colorize/", files={"file": ("test.jpg", open("test.jpg", "rb"), "image/jpeg")})
    assert response.status_code == 200  # Adjust for auth