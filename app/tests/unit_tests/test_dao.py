import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "user_id,is_present",
    [
        (1, True),
        (7, False),
    ],
)
async def test_find_user_by_id(user_id, is_present):
    user = await UserDAO.find_one_or_none(id=user_id)

    if is_present:
        assert user
        assert user["id"] == user_id
    else:
        assert not user
