from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text, Enum, Boolean
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class User(Base, AsyncAttrs):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)

    collections = relationship("Collection", back_populates="owner")

class Collection(Base, AsyncAttrs):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="collections")
    objects = relationship("Object", back_populates="collection", cascade="all, delete")

class ObjectStatus(enum.Enum):
    available = "В продаже"
    sold = "Продано"
    price_drop = "Снижение цены"
    price_up = "Повышение цены"
    removed = "Снято с продажи"

class Object(Base, AsyncAttrs):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, ForeignKey("collections.id"))

    location = Column(String)
    rooms_info = Column(String)
    area = Column(String)
    condition = Column(String)
    parking = Column(String)
    bathrooms = Column(Integer)
    extras = Column(Text)
    price = Column(String)

    status = Column(Enum(ObjectStatus), default=ObjectStatus.available)
    price_updated_at = Column(DateTime(timezone=True), default=None, nullable=True)
    sold_at = Column(DateTime(timezone=True), default=None, nullable=True)
    removed_at = Column(DateTime(timezone=True), default=None, nullable=True)

    collection = relationship("Collection", back_populates="objects")
    media = relationship("Media", back_populates="object", cascade="all, delete")

class Media(Base, AsyncAttrs):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey("objects.id"))
    file_id = Column(String)
    media_type = Column(String)  # 'photo' or 'video'

    object = relationship("Object", back_populates="media")

class Contact(Base, AsyncAttrs):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    is_active = Column(Boolean, default=True)
