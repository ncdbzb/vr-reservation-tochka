from fastapi import FastAPI, HTTPException
from app.schemas import EmailRequest
from app.email_service import EmailService

app = FastAPI()


@app.post("/send-email")
async def send_email(request: EmailRequest):
    # try:
    EmailService.send(
        user_email=request.user_email,
        subject=request.subject,
        body=request.body
    )
    return {"status": "success"}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
