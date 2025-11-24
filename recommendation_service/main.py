from fastapi import FastAPI
import contextlib
from rec_sys_mcp import mcp
import os

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan)
app.mount("/", mcp.streamable_http_app(), name="mcp")

PORT = os.getenv("PORT", "3000")