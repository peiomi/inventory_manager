from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from ..database.connection import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)