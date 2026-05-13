
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
        "image_path": "items/wooden_hammer.png",
        "can_restock": False,
        "restock_quantity": 0,
        "effect_value": 0,
        "consumable": False,
    },
    {
        "name": "Nails",
        "base_price": 5,
        "rarity": "common",
        "description": "Cheap, sturdy iron fasteners",
        "image_path": "items/nails.png",
        "can_restock": True,
        "restock_quantity": 200,
        "effect_value": 0,
        "consumable": False,
    },
    {
        "name": "Wooden Planks",
        "base_price": 10,
        "rarity": "common",
        "description": "Cedar planks, useful for building just about anything",
        "image_path": "items/planks.png",
        "can_restock": True,
        "restock_quantity": 100,
        "effect_value": 0,
        "consumable": False,
    },

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
    # 1. Create shop if missing
    if user.shop is None:
        shop = Shop(user_id=user.id, last_restock=None)
        db.session.add(shop)
        db.session.commit()
    else:
        shop = user.shop

    # 2. Ensure every item exists in the shop
    existing_items = {si.item_id: si for si in shop.items}

    for item in Item.query.all():
        if item.id not in existing_items:
            # New item added to the game → add to shop
            new_shop_item = ShopItem(
                shop_id=shop.id,
                item_id=item.id,
                quantity=item.restock_quantity
            )
            db.session.add(new_shop_item)

    db.session.commit()



