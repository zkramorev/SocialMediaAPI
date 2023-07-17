import enum
from sqlalchemy import Column, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship

from app.database import Base


class UserRelationship(Base):
    __tablename__ = "users_relationships"

    id = Column(Integer, primary_key=True, nullable=False)
    user_from_id = Column(Integer, ForeignKey("users.id"),  nullable=False)
    user_to_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    relationship_status = relationship("RelationshipTypes", back_populates="users_relationships")

class RelationshipTypes(enum.Enum):
    FRIENDS = "friends"
    SUBSCRIBER = "subscriber"
    SEND_FRIEND_REQUEST = "send_friends_request"

class RelationshipType(Base):
    __tablename__ = "relationship_types"
    
    id = Column(Integer, primary_key=True, nullable=False)
    relationship_status = Column(Enum(RelationshipTypes), unique=True, nullable=False)