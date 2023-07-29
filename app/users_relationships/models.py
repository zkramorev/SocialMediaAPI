from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, Integer, String

from app.database import Base


class UserRelationship(Base):
    __tablename__ = "users_relationships"

    id = Column(Integer, primary_key=True, nullable=False)
    user_from_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_to_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    relationship_status = Column(String, nullable=False)


@dataclass
class RelationshipTypes:
    FRIENDS: str = "friends"
    HAVE_FRIEND_REQUEST: str = "have_friends_request"
    SEND_FRIEND_REQUEST: str = "send_friends_request"
