from fastapi import HTTPException


def raise_user_not_found():
    raise HTTPException(404, "User not found")


def raise_user_already_registered():
    raise HTTPException(400, "Username already registered")
