from sqlalchemy.sql.functions import user

from app import db
from app.models import ShopInventory, Item, User
from app.extensions import db

# initial item add using if statements
# also need to distinguish one-time items from buyables/restockables restock flag?




def restock(user):
    ShopInventory.query.filter_by(user_id=user.id).delete()
    # potential bug: if user hasn't purchased one-time items that dont restock, they'll be softlocked here

    items = Item.query.all()

    for item in items:
        if item.can_restock:
            db.session.add(ShopInventory(user_id = user.id,
                                            item_id=item.id,
                                             quantity=item.restock_quantity))
    db.session.commit()





