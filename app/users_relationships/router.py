from fastapi import APIRouter, Depends
from app.users.dao import UserDAO
from app.users.models import User
from app.users.dependencies import get_current_user
from app.users_relationships.dao import UserRelDAO
from app.users_relationships.models import RelationshipTypes
from app.exceptions import CannotSendRequestToYourself, UserNotFound

router = APIRouter(
    prefix="/requests",
    tags=["User Request"]
)


@router.post("/new")
async def new_request(user_to_id: int, user_from: User = Depends(get_current_user)):
    
    user_to = await UserDAO.find_one_or_none(id=user_to_id)
    if user_to is None:
        raise UserNotFound
    if user_from.id == user_to_id:
        raise CannotSendRequestToYourself

    current_status_from_to = await UserRelDAO.find_one_or_none(user_from_id=user_from.id, user_to_id=user_to_id)

    if current_status_from_to is None:
        await UserRelDAO.add_new_one(user_from_id=user_from.id, user_to_id=user_to_id, relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST)
        await UserRelDAO.add_new_one(user_from_id=user_to_id, user_to_id=user_from.id, relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST)
    elif current_status_from_to.relationship_status == RelationshipTypes.HAVE_FRIEND_REQUEST:
        await UserRelDAO.add_new_one(user_from_id=user_to_id, user_to_id=user_from.id, relationship_status=RelationshipTypes.FRIENDS)
        await UserRelDAO.add_new_one(user_from_id=user_from.id, user_to_id=user_to_id, relationship_status=RelationshipTypes.FRIENDS)

        await UserRelDAO.delete_one(user_from_id=user_from.id, user_to_id=user_to_id, relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST)
        await UserRelDAO.delete_one(user_from_id=user_to_id, user_to_id=user_from.id, relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST)

@router.post("/acceptance")
async def accept_request(subscriber_id: int, current_user: User = Depends(get_current_user)):
    
    user_subscriber = await UserDAO.find_one_or_none(id=subscriber_id)
    if user_subscriber is None:
        raise UserNotFound
    if user_subscriber.id == current_user.id:
        raise CannotSendRequestToYourself
    
    current_status_from_to = await UserRelDAO.find_one_or_none(user_from_id=current_user.id, user_to_id=subscriber_id)
    if current_status_from_to.relationship_status == RelationshipTypes.HAVE_FRIEND_REQUEST:
        await UserRelDAO.add_new_one(user_from_id=current_user.id, user_to_id=user_subscriber.id, relationship_status=RelationshipTypes.FRIENDS)
        await UserRelDAO.add_new_one(user_from_id=user_subscriber.id, user_to_id=current_user.id, relationship_status=RelationshipTypes.FRIENDS)
        await UserRelDAO.delete_one(user_from_id=current_user.id, user_to_id=user_subscriber.id, relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST)
        await UserRelDAO.delete_one(user_from_id=user_subscriber.id, user_to_id=current_user.id, relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST)

@router.post("/rejection")
async def reject_request(subscriber_id: int, current_user: User = Depends(get_current_user)):
    
    user_subscriber = await UserDAO.find_one_or_none(id=subscriber_id)
    if user_subscriber is None:
        raise UserNotFound
    if user_subscriber.id == current_user.id:
        raise CannotSendRequestToYourself
    
    current_status_from_to = await UserRelDAO.find_one_or_none(user_from_id=current_user.id, user_to_id=subscriber_id)
    if current_status_from_to.relationship_status == RelationshipTypes.HAVE_FRIEND_REQUEST:
        await UserRelDAO.delete_one(user_from_id=current_user.id, user_to_id=user_subscriber.id, relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST)
        await UserRelDAO.delete_one(user_from_id=user_subscriber.id, user_to_id=current_user.id, relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST)

@router.get("/incoming")
async def get_subscribers(current_user: User = Depends(get_current_user)):
    subscribers_names = await UserRelDAO.get_requests(user_from_id=current_user.id, relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST)
    return subscribers_names

@router.get("/outgoing")
async def get_outgoing_requests(current_user: User = Depends(get_current_user)):
    outgoing_user_requests_names = await UserRelDAO.get_requests(user_from_id=current_user.id, relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST)
    return outgoing_user_requests_names


