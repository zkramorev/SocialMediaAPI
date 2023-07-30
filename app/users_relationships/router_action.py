from fastapi import APIRouter, Depends

from app.exceptions import CannotSendRequestToYourself, UserNotFound
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users_relationships.dao import UserRelDAO
from app.users_relationships.models import RelationshipTypes

router = APIRouter(prefix="/requests", tags=["User Request"])


@router.put("/new")
async def new_request(user_to_name: str, user_from: User = Depends(get_current_user)):
    user_to = await UserDAO.find_one_or_none(user_name=user_to_name)
    if user_to is None:
        raise UserNotFound
    if user_from.id == user_to.id:
        raise CannotSendRequestToYourself

    current_status_from_to = await UserRelDAO.find_one_or_none(
        user_from_id=user_from.id, user_to_id=user_to.id
    )

    if current_status_from_to is None:
        await UserRelDAO.add_new_one(
            user_from_id=user_from.id,
            user_to_id=user_to.id,
            relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST,
        )
        await UserRelDAO.add_new_one(
            user_from_id=user_to.id,
            user_to_id=user_from.id,
            relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST,
        )
    elif (
        current_status_from_to.relationship_status
        == RelationshipTypes.HAVE_FRIEND_REQUEST
    ):
        await UserRelDAO.add_new_one(
            user_from_id=user_to.id,
            user_to_id=user_from.id,
            relationship_status=RelationshipTypes.FRIENDS,
        )
        await UserRelDAO.add_new_one(
            user_from_id=user_from.id,
            user_to_id=user_to.id,
            relationship_status=RelationshipTypes.FRIENDS,
        )

        await UserRelDAO.delete_one(
            user_from_id=user_from.id,
            user_to_id=user_to.id,
            relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST,
        )
        await UserRelDAO.delete_one(
            user_from_id=user_to.id,
            user_to_id=user_from.id,
            relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST,
        )


@router.put("/acceptance")
async def accept_request(
    subscriber_name: str, current_user: User = Depends(get_current_user)
):
    user_subscriber = await UserDAO.find_one_or_none(user_name=subscriber_name)
    if user_subscriber is None:
        raise UserNotFound
    if user_subscriber.id == current_user.id:
        raise CannotSendRequestToYourself

    current_status_from_to = await UserRelDAO.find_one_or_none(
        user_from_id=current_user.id, user_to_id=user_subscriber.id
    )
    if (
        current_status_from_to.relationship_status
        == RelationshipTypes.HAVE_FRIEND_REQUEST
    ):
        await UserRelDAO.add_new_one(
            user_from_id=current_user.id,
            user_to_id=user_subscriber.id,
            relationship_status=RelationshipTypes.FRIENDS,
        )
        await UserRelDAO.add_new_one(
            user_from_id=user_subscriber.id,
            user_to_id=current_user.id,
            relationship_status=RelationshipTypes.FRIENDS,
        )
        await UserRelDAO.delete_one(
            user_from_id=current_user.id,
            user_to_id=user_subscriber.id,
            relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST,
        )
        await UserRelDAO.delete_one(
            user_from_id=user_subscriber.id,
            user_to_id=current_user.id,
            relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST,
        )


@router.put("/rejection")
async def reject_request(
    subscriber_name: str, current_user: User = Depends(get_current_user)
):
    user_subscriber = await UserDAO.find_one_or_none(user_name=subscriber_name)
    if user_subscriber is None:
        raise UserNotFound
    if user_subscriber.id == current_user.id:
        raise CannotSendRequestToYourself

    current_status_from_to = await UserRelDAO.find_one_or_none(
        user_from_id=current_user.id, user_to_id=user_subscriber.id
    )
    if (
        current_status_from_to.relationship_status
        == RelationshipTypes.HAVE_FRIEND_REQUEST
    ):
        await UserRelDAO.delete_one(
            user_from_id=current_user.id,
            user_to_id=user_subscriber.id,
            relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST,
        )
        await UserRelDAO.delete_one(
            user_from_id=user_subscriber.id,
            user_to_id=current_user.id,
            relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST,
        )


@router.delete("/deleting_friend")
async def delete_friend(
    friend_name: str, current_user: User = Depends(get_current_user)
):
    user_friend = await UserDAO.find_one_or_none(user_name=friend_name)
    if user_friend is None:
        raise UserNotFound
    if user_friend.id == current_user.id:
        raise CannotSendRequestToYourself

    current_status_from_to = await UserRelDAO.find_one_or_none(
        user_from_id=current_user.id, user_to_id=user_friend.id
    )
    if current_status_from_to.relationship_status == RelationshipTypes.FRIENDS:
        await UserRelDAO.add_new_one(
            user_from_id=current_user.id,
            user_to_id=user_friend.id,
            relationship_status=RelationshipTypes.HAVE_FRIEND_REQUEST,
        )
        await UserRelDAO.add_new_one(
            user_from_id=user_friend.id,
            user_to_id=current_user.id,
            relationship_status=RelationshipTypes.SEND_FRIEND_REQUEST,
        )
        await UserRelDAO.delete_one(
            user_from_id=current_user.id,
            user_to_id=user_friend.id,
            relationship_status=RelationshipTypes.FRIENDS,
        )
        await UserRelDAO.delete_one(
            user_from_id=user_friend.id,
            user_to_id=current_user.id,
            relationship_status=RelationshipTypes.FRIENDS,
        )
