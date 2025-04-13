#自定义中间件实现token鉴权
from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings


class JwtAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        #请求白名单，也就是不需要进行token鉴权的请求
        white_list = ["/user/login",
                      "/user/email_send",
                      "/user/register",
                      '/project/getproject-pass',
                      '/project/category',
                      '/project_operate/categroy_name',
                      '/project_operate/search-ByTime',
                     '/project_operate/search',
                      ]
        path = request.path
        if path not in white_list and not path.startswith("/media"):
            #从头文件中获取token,前端在处理时，也要把token放在头文件
            token = request.META.get('HTTP_AUTHORIZATION')
            # print("token",token)
            #验证token
            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                return JsonResponse({"code":"401","info":"Token过期，请重新登录"})
            except InvalidTokenError:
                return JsonResponse({"code": "401", "info": "Token验证失败"})
            except PyJWTError:
                return JsonResponse({"code": "401", "info": "Token验证异常"})

        else:
            return None