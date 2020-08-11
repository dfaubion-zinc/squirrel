import configparser
import random

from squirrel.model import Order, OrderItem, Listing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = configparser.ConfigParser()
config.read('alembic.ini')
engine = create_engine(config['alembic']['sqlalchemy.url'], echo=True)

Session = sessionmaker(engine)

def do_add():
    session = Session()
    order = Order(name="order_" + str(random.randint(0, 2 ** 32)))
    session.add(order)
    
    listing = Listing(name="listing_" + str(random.randint(0, 2 ** 32)))
    session.add(listing)
    session.flush()
    session.commit()

    session = Session()
    order_item = OrderItem(
        name="order_item_" + str(random.randint(0, 2 ** 32)),
        listing_id = listing.id,
        order_id = order.id
    )
    session.add(order_item)
    session.commit()



def do_main():
    print("\n\ndo_main\n\n")
    session = Session()
    items = session\
        .query(Order, OrderItem, Listing)\
        .filter(
            Order.id == OrderItem.order_id,
            Listing.id == OrderItem.listing_id
        )\
        .all()

    items = [(item[0], item[1], item[2]) for item in items]

    print("should be done querying")
    for item in items:
        print("\n\n", item[0].id, item[1].id, item[2].id, "\n\n")
    
    


if __name__ == "__main__":
    do_add()
    do_main()