from datetime import date, datetime
from sqlmodel import Enum, Relationship, SQLModel, Field

# class OrderStatus(Enum):
#     PENDING = "pending"
#     COMPLETED = "completed"
#     CANCELED = "canceled"


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False, index=True)
    password: str = Field(nullable=False)
    phone: str = Field(nullable=True, max_length=15)
    birth_date: date | None = Field(default=None, nullable=True)


class Restaurants(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False, index=True)
    phone: str = Field(nullable=False, max_length=15)
    password: str = Field(nullable=False)


class Recipes(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None, nullable=True)
    price: float = Field(nullable=False)
    photo: str | None = Field(default=None, nullable=True)
    category: str | None = Field(nullable=True, index=True)
    restaurant_id: int = Field(foreign_key="restaurants.id")


class Orders(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: datetime | None = Field(default_factory=datetime.now, nullable=False)
    status: str = Field(default="pending", nullable=False)
    restaurant_id: int = Field(foreign_key="restaurants.id")
    user_id: int = Field(foreign_key="users.id")


class Order_Details(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    recipe_id: int = Field(foreign_key="recipes.id")
    quantity: int = Field(default=1, nullable=False , gt=0)
