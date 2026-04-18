from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserLogin, UserRead
from app.services.auth import authenticate_user, create_access_token, get_password_hash
from app.core.config import get_settings


router = APIRouter(tags=["Authentication"])


async def _parse_request_data(request: Request) -> dict:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        return await request.json()
    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        return dict(await request.form())
    return {}


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, db: Session = Depends(get_db)):
    data = await _parse_request_data(request)
    payload = UserCreate(**data)

    existing_user = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=Token)
async def login_user(request: Request, db: Session = Depends(get_db)):
    data = await _parse_request_data(request)
    payload = UserLogin(**data)

    user = authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    settings = get_settings()
    token = create_access_token({"sub": str(user.id)}, settings=settings)
    return Token(access_token=token)

