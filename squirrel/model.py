import sqlalchemy as sa
import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    __tablename__ = "order"
    id = Column(postgresql.UUID, primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String)

    items = sa.orm.relationship("OrderItem", back_populates='order')
    details = sa.orm.relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "order_detail"
    id = Column(postgresql.UUID, primary_key=True, default=lambda: uuid.uuid4().hex)
    order_id = Column(postgresql.UUID, sa.ForeignKey('order.id'), index=True)
    name = Column(String)

    order = sa.orm.relationship("Order", back_populates='details')


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(postgresql.UUID, primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String)
    order_id = Column(postgresql.UUID, sa.ForeignKey('order.id'), index=True)
    listing_id = Column(postgresql.UUID, sa.ForeignKey('listing.id'), index=True)

    order = sa.orm.relationship("Order", back_populates='items')
    listing = sa.orm.relationship("Listing")


class Listing(Base):
    __tablename__ = "listing"
    id = Column(postgresql.UUID, primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String)

    items = sa.orm.relationship("ListingItem", back_populates='listing', lazy="joined")

class ListingItem(Base):
    __tablename__ = "listing_item"
    id = Column(postgresql.UUID, primary_key=True, default=lambda: uuid.uuid4().hex)
    listing_id = Column(postgresql.UUID, sa.ForeignKey('listing.id'), index=True)
    name = Column(String)
    listing = sa.orm.relationship("Listing")
