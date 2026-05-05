from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from app.extensions import db


class Todo(db.Model):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    xp: Mapped[int] = mapped_column(Integer, default=10)
    coins: Mapped[int] = mapped_column(Integer, default=5)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    xp_given: Mapped[bool] = mapped_column(Boolean, default=False)
    coins_received: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="todos")


class CompletedQuest(db.Model):
    __tablename__ = "completed_quests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    xp: Mapped[int] = mapped_column(Integer, nullable=False)
    date_completed: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="completed_quests")


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

    level: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String(250), nullable=False, default="Task Sapling")
    current_xp: Mapped[int] = mapped_column(Integer, default=0)
    next_level_xp: Mapped[int] = mapped_column(Integer, default=100)
    current_coins: Mapped[int] = mapped_column(Integer, default=0)

    quests_completed: Mapped[int] = mapped_column(Integer, default=0)
    last_bonus_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    todos = relationship("Todo", back_populates="user", cascade="all, delete")
    completed_quests = relationship("CompletedQuest", back_populates="user", cascade="all, delete")
    inventory: Mapped["Inventory"] = relationship(
        "Inventory",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

class Item(db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    base_price: Mapped[int] = mapped_column(Integer, nullable=False)
    rarity: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)

    inventory = relationship("Inventory", back_populates="item")
    shop_inventory = relationship("ShopInventory", back_populates="item")





class Inventory(db.Model):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    item = relationship("Item", back_populates="inventory")
    user = relationship("User", back_populates="inventory")

class ShopInventory(db.Model):
    __tablename__ = "shop_inventory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    item = relationship("Item", back_populates="shop_inventory")
    user = relationship("User", back_populates="shop_inventory")


