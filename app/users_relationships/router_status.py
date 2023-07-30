from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.exceptions import CannotSendRequestToYourself, UserNotFound
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users_relationships.dao import UserRelDAO
from app.users_relationships.models import RelationshipTypes

router = APIRouter(prefix="/statuses", tags=["User Statuses"])


@router.get("/incoming")
@cache(expire=30)
async def get_subscribers(current_user: User = Depends(get_current_user)):
    subscribers_names = await UserRelDAO.get_requests(
        user_from_id=current_user.id,
        relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST,
    )
    return subscribers_names


@router.get("/outgoing")
@cache(expire=30)
async def get_outgoing_requests(current_user: User = Depends(get_current_user)):
    outgoing_user_requests_names = await UserRelDAO.get_requests(
        user_from_id=current_user.id,
        relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST,
    )
    return outgoing_user_requests_names


@router.get("/friends")
@cache(expire=30)
async def get_outgoing_requests(current_user: User = Depends(get_current_user)):
    friends_names = await UserRelDAO.get_requests(
        user_from_id=current_user.id, relationship_status=RelationshipTypes.FRIENDS
    )
    return friends_names


@router.get("/status")
async def get_current_status_with_user(
    user_name: str, current_user: User = Depends(get_current_user)
):
    user_to = await UserDAO.find_one_or_none(user_name=user_name)
    if user_to is None:
        raise UserNotFound
    if user_to.id == current_user.id:
        raise CannotSendRequestToYourself

    relationship_data = await UserRelDAO.find_one_or_none(
        user_from_id=current_user.id, user_to_id=user_to.id
    )
    if relationship_data is None:
        return "no relationship with this user"
    return relationship_data["relationship_status"]
