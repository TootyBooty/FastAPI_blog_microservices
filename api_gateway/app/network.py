import async_timeout
from aiohttp import ClientSession
from core.config import Config
from fastapi import HTTPException


async def make_request(
    session: ClientSession,
    url: str,
    method: str,
    data: dict = {},
    params: dict = {},
    headers: dict = {},
    authorized_user: dict = None,
):
    headers["api-gateway-token"] = Config.API_GATEWAY_TOKEN

    if authorized_user:
        data["authorized_user"] = authorized_user

    with async_timeout.timeout(Config.GATEWAY_TIMEOUT):
        async with session:
            request = getattr(session, method)
            async with request(
                url, json=data, params=params, headers=headers
            ) as response:
                data = await response.json()
                if response.status > 399:
                    raise HTTPException(status_code=response.status, detail=data)
                return data
