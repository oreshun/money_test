
import json
import os
import random
import string
from datetime import datetime, timedelta
from email.policy import default

from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views import View
from rest_framework_jwt.settings import api_settings

from user.models import User, UserSerializer


# Create your views here.

#测试模块
class TestView(View):
    def get(self, request):
        #首先获取用户
        user = User.objects.filter(username='lisi',password='123456').first()
        if user:
            return JsonResponse({"code": 200, "info": "测试"})
        else:
            return JsonResponse({"code": 401, "info": "测试"})
#登录模块
class LoginView(View):
    def post(self, request):
        #获取前端发来的post数据
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        #打印一下，查看是否收到前端发来的信息
        print(email, password)
        #捕获异常
        try:
            #获取用户数据
            user = User.objects.get(user_email=email, password=password)
            #检查用户的账号状态，0为正常，1为禁用
            if user.status == 1:
                return JsonResponse({'code':500,'info':'该账户已经被禁用'})
            #下面将进行token的发送
            #首先获取jwt中的方法
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            # 编码处理
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            #将用户对象传进去，获取到独属于该对象的属性
            payload = jwt_payload_handler(user)
            #将属性编码转化为jwt格式的字符串
            token = jwt_encode_handler(payload)
        except Exception as e:
            print(e)
            return JsonResponse({"code": 500, 'info': '邮箱或密码错误'})

        return JsonResponse({"code": 200, "info": "登录成功",'token': token,'user':UserSerializer(user).data})

#注册模块
class RegisterView(View):
    def post(self, request):
        #从请求体中解析数据
        data = json.loads(request.body)
        useremail = data['useremail']
        username = data['username']
        password = data['password']
        operate = data['operate']
        try:
            # 首先查看数据库种是否已经存在当前email
            user2 = User.objects.filter(user_email=useremail).first()
            if user2 is not None:
                # 如果已经存在，则返回错误信息，并且说明用户已经存在
                return JsonResponse({"code": 500, 'info': '用户已经存在'})
            # 不存在，就进行添加
            # 在这里进行注册的只能是普通用户,user是已经保存的数据
            if operate == 'u':
                user = User.objects.create(username=username, password=password, user_email=useremail, identify="user")
            elif operate == 'm':
                user = User.objects.create(username=username, password=password, user_email=useremail, identify="manager")
        except Exception as e:
            print(e)
            return JsonResponse({"code": 500, 'info': '异常错误'})

        return JsonResponse({"code": 200, "info": "用户创建成功"})



#用户更换头像功能实现
class upload_avatarView(View):
    def post(self, request):
        #判断前端给的数据是否包含avatar键值对
        if request.FILES.get('avatar'):
            avatar = request.FILES['avatar']
            email = request.POST['useremail']#获取前端返回的邮箱
            #获取当前时间并格式化为字符串
            current_time = now().strftime('%Y%m%d%H%M%S')
            #获取文件扩展名
            file_extension = os.path.splitext(avatar.name)[1]
            #生成新的文件名
            new_filename = f'{email}_{current_time}{file_extension}'
            #存储文件
            file_path = default_storage.save(f"userAvatar/{new_filename}", avatar)
            file_url = file_path[11:]
            #更改数据库里用户的头像路径
            user = User.objects.get(user_email=email)
            user.avatar=file_url
            #保存修改
            user.save()
            #返回响应结果
            return JsonResponse({"code":200,"new_avatar_url":file_url})

        #如果没上传文件
        return JsonResponse({"code": 401, "message": "请上传头像！！"})

#用户更新个人信息功能实现
class upload_user_infomationView(View):
    def post(self, request):
        # 获取前端传递的所有信息
        or_email = request.POST.get('or_email')  # 使用 .get() 避免 KeyError
        # bith = request.POST['user_birthday']
        # print(bith)
        try:
            # 获取用户对象
            user = User.objects.get(user_email=or_email)

            # 处理每一个字段
            for key, value in request.POST.items():
                if key != 'or_email':  # 排除原邮箱字段
                    if hasattr(user, key):  # 判断模型中是否有该字段
                        if key == 'user_birthday':
                            if value:
                                try:
                                    # 检查日期格式并加一天
                                    user_birthday = datetime.strptime(value, '%Y-%m-%d').date() + timedelta(days=1)
                                    setattr(user, key, user_birthday)  # 更新出生日期字段
                                except ValueError as e:
                                    return JsonResponse({"code": 400, "info": f"日期格式错误，应为YYYY-MM-DD: {str(e)}"})
                            else:
                                continue
                        else:
                            setattr(user, key, value)  # 其他字段直接更新

                    # 判断是否修改了user_email字段
                    if key == 'user_email' and value != or_email:
                        # 如果修改了邮箱，检查是否已被注册
                        user_1 = User.objects.filter(user_email=value).first()
                        if user_1 is not None:
                            return JsonResponse({"code": 401, "info": "该邮箱已被注册！！"})

            # 保存更新后的用户信息
            user.save()

            return JsonResponse({"code": 200, "info": "信息更新成功！！","user":UserSerializer(user).data})

        except User.DoesNotExist:
            return JsonResponse({"code": 404, "info": "用户不存在"})
        except Exception as e:
            return JsonResponse({"code": 500, "info": f"服务器错误: {str(e)}"})
