from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, String, Integer
from marshmallow import ValidationError
from typing import List, Optional

#import os

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Yeshua2025%40%23@localhost/flask_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating our Base Model
class Base(DeclarativeBase):
    pass
#Initialize extensions
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma= Marshmallow(app)
# Initialize SQLAlchemy and Marshmallow db= SQL

#Association Table
user_pet = Table(
    "user_pet",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("pet_id", ForeignKey("pets.id")),
)

# User model
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100),nullable = False)
    email: Mapped[Optional[str]] = mapped_column(String(200), unique = True)

     # One-to-Many 
    pets: Mapped[List["Pet"]] = relationship(secondary = user_pet, back_populates="owners")

# Pet model
class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    animal: Mapped[str] = mapped_column(String(100))

    # One-to-Many
    owners: Mapped[List["User"]] = relationship(secondary=user_pet, back_populates="pets")


if __name__ == "__main__":
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(debug=True)