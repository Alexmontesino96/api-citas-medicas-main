from fastapi import APIRouter

get_welcome_message = APIRouter()

@get_welcome_message.get("/", tags=["welcome_message"])
async def welcome_message():
    return {"message": "Welcome to Medical Center API"}