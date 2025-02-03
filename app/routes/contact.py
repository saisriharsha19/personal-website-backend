from fastapi import APIRouter, HTTPException, status, Depends
from app.database import add_contact_message  # Changed import
from app.models import ContactMessageCreate, ContactMessageResponse
from typing import Annotated

router = APIRouter(tags=["Contact"])


@router.post("/")
async def send_contact_message(message: ContactMessageCreate):
    try:
        new_message = add_contact_message(
            name=message.name,
            email=message.email,
            message=message.message
        )
        return new_message
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
