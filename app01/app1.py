import re
from ninja import NinjaAPI, Schema

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
@costumers.post("/add", response={400: Error, 200: Success})
def add(request, data: Customer_ADD_Schema):
    for k, v in data.dict().items():
        print(k, v)
    if data.gender != 1 and data.gender != 2:
        return 400, {"msg": "性别只能是1或者2"}
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, data.email) is None:
        return 400, {"msg": "邮箱格式不正确"}

    models.Customer.objects.create(**data.dict())
    return 200, {"status": "success", "msg": "添加成功"}

# 查询客户（全部）
class Customer_SHOW_Schema(Schema):
    name: str
    email: str
    gender: int
@costumers.get("/show")
def show(request, data: Customer_SHOW_Schema):
     customers_list = models.Customer.objects.all()
     return customers_list