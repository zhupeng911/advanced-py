from typing import Optional

from sqlalchemy.orm import Session

from core.po.shop import Shop
from core.vo.base import ShopCreateVo


def get_all_shops(db: Session) -> list[Shop]:
    return db.query(Shop).all()


def get_shop_by_id(db: Session, shop_id: int) -> Optional[Shop]:
    return db.query(Shop).filter(Shop.id == shop_id).first()


def create_shop(db: Session, vo: ShopCreateVo) -> Shop:
    shop = Shop(name=vo.name, counter=vo.counter, price=vo.price)
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop
