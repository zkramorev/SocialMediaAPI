from fastapi import APIRouter, Response
from app.users.schemas import SUserAuth
from app.users.dao import UserDAO
from app.users.auth import get_password_hash, create_access_token, verify_password
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user_email = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user_email:
        raise UserAlreadyExistsException
    existing_user_user_name = await UserDAO.find_one_or_none(user_name=user_data.user_name)
    if existing_user_user_name:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add_new_one(email=user_data.email, hashed_password=hashed_password, user_name=user_data.user_name)

@router.post("/login")
async def register_user(response: Response, user_data: SUserAuth):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user is None:
        raise IncorrectEmailOrPasswordException
    if not verify_password(user_data.password, user.hashed_password):
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": user.id})
    response.set_cookie("social_media_access_token", access_token, httponly=True)
    return {"access_token": access_token}
    