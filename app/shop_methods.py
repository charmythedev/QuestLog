
from app.extensions import db

from app.models import Shop, Item, ShopItem, User
from app.extensions import db

# initial item add using if statements
# also need to distinguish one-time items from buyables/restockables restock flag?

from app.models import Item
from app.extensions import db

ITEM_DEFINITIONS = [
    {
        "name": "Steam Potion",
        "base_price": 100,
        "rarity": "common",
        "description": "A bottle full of steam, restores energy.",
        "image_path": "items/steam_potion.png",
        "can_restock": True,
        "restock_quantity": 10,
        "effect_value": 5,
        "consumable": True,
    },
    {
        "name": "Wooden Hammer",
        "base_price": 500,
        "rarity": "rare",
        "description": "A sturdy wooden hammer.",
        "image_path": "items/hammer.png",
        "can_restock": False,
        "restock_quantity": 1,
        "effect_value": 0,
        "consumable": False,
    },
    # Add more items here...
]


def seed_items():
    for data in ITEM_DEFINITIONS:
        item = Item.query.filter_by(name=data["name"]).first()

        if item:
            # Update existing item
            for key, value in data.items():
                setattr(item, key, value)
        else:
            # Create new item
            item = Item(**data)
            db.session.add(item)

    db.session.commit()
    print("Items seeded/updated successfully.")


def use_item(item):
    if item.name == "Steam Potion":
        pass



def restock_shop(shop):
    for shop_item in shop.items:
        item = shop_item.item

        if item.can_restock:
            shop_item.quantity = item.restock_quantity


def seed_shop_for_user(user):
    # If shop exists, do nothing
    if user.shop is not None:
        return

    shop = Shop(user_id=user.id, last_restock=None)
    db.session.add(shop)
    db.session.commit()

    # Add items to the shop
    for item in Item.query.all():
        db.session.add(ShopItem(
            shop_id=shop.id,
            item_id=item.id,
            quantity=item.restock_quantity
        ))

    db.session.commit()



