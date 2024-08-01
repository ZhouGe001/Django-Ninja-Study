import json

from django.http import JsonResponse
import re
from django.utils.deprecation import MiddlewareMixin

class EmailValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = [
            '/costumers/add/',
        ]
        # 判断url是否在path列表中
        if request.path not in path:
            return None
        # 读取request中的数据，并转换为字符串
        # 注意，在django ninja中，读取数据不能使用request.POST.get('email')，该值为None
        data_str = request.body.decode('utf-8')     # request.body 是一个bytes类型，其内容是传输过来的json数据
        # 将字符串转换为字典
        data_dict = json.loads(data_str)

        email = data_dict['email']
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, email) is None:
            return JsonResponse({'status': 'error', 'msg': '邮箱格式不正确'}, status=400)

        # 如果邮箱格式正确，继续处理请求
        return self.get_response(request)

