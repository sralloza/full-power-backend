from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from pydantic.main import BaseModel

router = APIRouter()


class User(BaseModel):
    username: str
    password: str


valid_users = [("mark", "asdf"), ("user", "password")]
valid_users = [User(username=a, password=b) for (a, b) in valid_users]


@router.post("/login")
def login_endpoint(user: User):
    """Login endpoint."""
    if user not in valid_users:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"status": "ok"}


@router.post("/logout")
def logout_endpoint():
    """Logout endpoint."""
    return "logout-endpoint"
