import uvicorn

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
# from fastapi_jsonrpc import API, JsonRpcRouter
from src.auth.auth_router import router as auth_router
from src.services.celery_service import send_email_task

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

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/send_mail")
async def send_mail():
    result = send_email_task.delay('kostya.pershin.18@mail.ru')
    result = result.get()
    print(f"RESULTRESULTRESULT: {result}")
    if result == 'success':
        return {'status': 'success'}
    else:
        raise HTTPException(status_code=500, detail='error')


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )