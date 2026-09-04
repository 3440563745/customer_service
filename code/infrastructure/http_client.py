import asyncio

import httpx
from httpx import AsyncClient
# httpx_client=httpx.AsyncClient()
httpx_client:AsyncClient|None=None
def init_http_client():
    global httpx_client
    httpx_client=AsyncClient()

async def close_http_client():
    await httpx_client.aclose()

if __name__=="__main__":
    async def test():
        init_http_client()
        result=await httpx_client.get("http://localhost:18081/users/u1001/orders")
        print(result.json()["data"]["orders"][0])
        await close_http_client()



    asyncio.run(test())