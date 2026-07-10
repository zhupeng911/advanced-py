from fastapi import APIRouter, Path, Query

from vo.shop import ShopCreateVo

# 创建购物车模块的分路由
shop_route = APIRouter(tags=["购物车模块接口"])


# 1.获取所有购物车
@shop_route.get("/get_all", summary="获取所有购物车", description="获取所有购物车的接口")
def get_all_shop():
    print("获取所有购物车")
    shop_list = [{"id": 1, "name": "购物车1"}, {"id": 2, "name": "购物车2"}]
    return {"msg": "购物车列表", "data": shop_list}


# 2.获取购物车详情【路由传参】
@shop_route.get("/get_detail/{id}", summary="获取购物车详情", description="获取购物车详情的接口")
def get_shop_detail(id: int = Path(..., description="购物车ID")):
    print("获取购物车详情")
    shop_detail = {"id": id, "name": "购物车1", "items": [{"id": 1, "name": "商品1"}, {"id": 2, "name": "商品2"}]}
    return {"msg": "购物车详情", "data": shop_detail}


# 3.获取购物车详情【URL传参】
@shop_route.get("/get_detail_by_id", summary="获取购物车详情", description="获取购物车详情的接口")
def get_shop_detail_by_id(id: int = Query(..., description="购物车ID")):
    print("获取购物车详情")
    shop_detail = {"id": id, "name": "购物车1", "items": [{"id": 1, "name": "商品1"}, {"id": 2, "name": "商品2"}]}
    return {"msg": "购物车详情", "data": shop_detail}


# 4.创建购物车【请求体传参】
@shop_route.post("/create", summary="创建购物车", description="创建购物车的接口")
def create_shop(shop: ShopCreateVo):
    print(shop)
    return {"msg": "购物车创建成功", "data": {"id": 1, "name": shop.name}}
