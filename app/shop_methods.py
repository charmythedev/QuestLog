
from app.extensions import db

from app.models import Shop, Item, ShopItem, User
from app.extensions import db

# initial item add using if statements
# also need to distinguish one-time items from buyables/restockables restock flag?



def restock_shop(shop):
    for shop_item in shop.items:
        item = shop_item.item

        if item.can_restock:
            shop_item.quantity = item.restock_quantity


def seed_items():
    if Item.query.count() > 0:
        return  # already seeded

    items = [
        Item(name="Steam Potion", base_price=100, rarity="common",
             description="A bottle full of steam, allows adventurers to keep questing",
             image_path= "items/steam_potion.png",
             restock_quantity=10),

        Item(name="Wooden Hammer", base_price=500, rarity="rare",
             description="A useful tool", can_restock=False, restock_quantity=1,
             image_path= "items/wooden_hammer.png"),

        Item(name="Wooden Planks", base_price=10, rarity="common",
             description="Cedar planks for building all sorts of things",
             restock_quantity=100),

        Item(name="Nails", base_price=5, rarity="common",
             description="Quick, cheap iron fasteners",
             restock_quantity=100)
    ]

    for i in items:
        db.session.add(i)

    db.session.commit()

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



