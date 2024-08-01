import re
from typing import List
from ninja import NinjaAPI, Schema, Query
from django.db.models import Q
from ninja.errors import ValidationError

from app01 import models

costumers = NinjaAPI()

# 添加客户
class Customer_ADD_Schema(Schema):
    username: str
    password: str
    email: str
    gender: int
class Error(Schema):
    msg: str
class Success(Schema):
    status: str
    msg: str
@costumers.post("/add/", response={200: Success})
def add(request, data: Customer_ADD_Schema):
    # print(request.POST.get('email'))        # 输出为None
    if data.gender not in [1, 2]:
        raise ValidationError({"massage": "性别只能是1或者2"})

    # 该部分已在中间件中实现
    # pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # if re.match(pattern, data.email) is None:
    #     raise ValidationError({"massage": "邮箱格式不正确"})

    models.Customer.objects.create(**data.dict())
    return 200, {"status": "success", "msg": "添加成功"}

# 查询客户（全部）
class Customer_SHOW_Schema(Schema):
    username: str
    email: str
    gender: int
@costumers.get("/show_all/", response=List[Customer_SHOW_Schema])
def show_all(request):
     customers_list = models.Customer.objects.all()
     return customers_list


# 查询客户（单个）
class Customer_SHOW_Schema_IN(Schema):
    # 可以为空
    username: str = None
    email: str = None
@costumers.get("/show/", response={200: List[Customer_SHOW_Schema], 400: Error})
# ... 必填
def show_one(request, data: Customer_SHOW_Schema_IN=Query(...)):
    # 查询关系为“或”
    customer = models.Customer.objects.filter(Q(username=data.username) | Q(email=data.email))
    if customer:
        return customer
    else:
        return 400, {"msg": "客户不存在"}

# 删除客户
@costumers.delete("{id}/delete/", response={200: Success, 400: Error})
def delete(request, id: int):
    try:
        models.Customer.objects.get(id=id).delete()
        return 200, {"status": "success", "msg": "删除成功"}
    except:
        return 400, {"msg": "客户不存在"}

# 更新客户
class Customer_UPDATE_Schema(Schema):
    username: str
    email: str
    gender: int
@costumers.put("{id}/update/", response={200: Success, 400: Error})
def update(request, id: int, data: Customer_UPDATE_Schema):
    try:
        customer = models.Customer.objects.get(id=id)
        for k, v in data.dict().items():
            if v:
                setattr(customer, k, v)
        customer.save()
        return 200, {"status": "success", "msg": "更新成功"}
    except:
        return 400, {"msg": "客户不存在"}

