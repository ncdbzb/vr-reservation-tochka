import uvicorn
import asyncio
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
# from fastapi_jsonrpc import API, JsonRpcRouter
from src.auth.auth_router import router as auth_router
from src.auth.utils.create_user import create_admin_user
from src.routers.users_router import router as users_router

from config.config import CORS_ORIGINS


app = FastAPI(
    title="vr_reservation",
    root_path="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/auth"
)
app.include_router(
    users_router,
    prefix="/users"
)

# @app.get("/send_mail")
# async def send_mail():
#     result = send_email_task.delay('kostya.pershin.18@mail.ru')
#     result = result.get()
#     if result == 'success':
#         return {'status': 'success'}
#     else:
#         raise HTTPException(status_code=500, detail='error')

async def main():
    await create_admin_user()

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000
    )
    server = uvicorn.Server(config)
    await server.serve()
    

if __name__ == "__main__":
    asyncio.run(main())
