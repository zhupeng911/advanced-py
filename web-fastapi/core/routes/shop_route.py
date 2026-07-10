from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from depends.depends import get_db
from core.service import shop_service
from vo.shop import ShopCreateVo

# 创建购物车模块的分路由
shop_route = APIRouter(tags=["购物车模块接口"])


# 1.获取所有购物车
@shop_route.get("/get_all", summary="获取所有购物车", description="获取所有购物车的接口")
def get_all_shop(db: Session = Depends(get_db)):
    shops = shop_service.get_all_shops(db)
    return {
        "msg": "购物车列表",
        "data": [{"id": s.id, "name": s.name, "counter": s.counter, "price": s.price} for s in shops],
    }


# 2.获取购物车详情【路由传参】
@shop_route.get("/get_detail/{id}", summary="获取购物车详情", description="获取购物车详情的接口")
def get_shop_detail(id: int = Path(..., description="购物车ID"), db: Session = Depends(get_db)):
    shop = shop_service.get_shop_by_id(db, id)
    if shop is None:
        raise HTTPException(status_code=404, detail=f"购物车 {id} 不存在")
    return {"msg": "购物车详情", "data": {"id": shop.id, "name": shop.name, "counter": shop.counter, "price": shop.price}}


# 3.获取购物车详情【URL传参】
@shop_route.get("/get_detail_by_id", summary="获取购物车详情", description="获取购物车详情的接口")
def get_shop_detail_by_id(id: int = Query(..., description="购物车ID"), db: Session = Depends(get_db)):
    shop = shop_service.get_shop_by_id(db, id)
    if shop is None:
        raise HTTPException(status_code=404, detail=f"购物车 {id} 不存在")
    return {"msg": "购物车详情", "data": {"id": shop.id, "name": shop.name, "counter": shop.counter, "price": shop.price}}


# 4.创建购物车【请求体传参】
@shop_route.post("/create", summary="创建购物车", description="创建购物车的接口")
def create_shop(shop: ShopCreateVo, db: Session = Depends(get_db)):
    created = shop_service.create_shop(db, shop)
    return {"msg": "购物车创建成功", "data": {"id": created.id, "name": created.name, "counter": created.counter, "price": created.price}}
