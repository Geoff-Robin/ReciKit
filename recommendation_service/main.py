from fastapi import FastAPI
import contextlib
from recommendation import mcp_app
import os


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp_app.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/", mcp_app.streamable_http_app(), name="mcp")
PORT = os.getenv("PORT", "3000")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(PORT))
