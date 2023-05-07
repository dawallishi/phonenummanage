from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1.不用登录就能访问的处理
        if request.path_info in ['/login/', '/img/code/']:
            return

        # 2.获取session信息
        info_dict = request.session.get('info')

        # 未登录
        if not info_dict:
            return redirect('/login/')

        # 已登陆
        request.info_dict = info_dict
