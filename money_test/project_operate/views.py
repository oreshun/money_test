import json
import mimetypes
import os.path
import uuid
from datetime import datetime
from mimetypes import guess_type
from urllib.parse import quote

import cx_Oracle
from celery.bin.control import status
from django.contrib.admin.templatetags.admin_list import results
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.cache import cache
from django.db import connection
from django.db.transaction import commit
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render
from django.template.defaultfilters import title
from django.template.defaulttags import comment
from django.utils.timezone import now
from django.views import View
from unicodedata import category

from money_test import settings
from project_operate.models import t_investment, t_favorite, t_comment, t_commentSerializer, t_comment_reply
from project_test.models import t_project, t_project_Serializer, t_category, CategorySerializer


# Create your views here.
#执行投资操作
def project_investment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #获取数据
        project_id = data['project_id']
        user_id =data['user_id']
        amount = data['amount']
        #更改该项目的募集金额
        p = t_project.objects.get(project_id=project_id)
        p.raised_amount = p.raised_amount + amount
        p.save()
        try:
            #如果没报错，说明此人之前就已经投资过这个项目
            t = t_investment.objects.get(project_id=project_id, user_id=user_id)
            t.amount = t.amount + amount
            t.save()
            return JsonResponse({'code':201,'info':'再次投资此项目成功！！'})
        except t_investment.DoesNotExist:
            #如果不存在，说明之前没投资此项目
            s = t_investment(project_id=project_id, user_id=user_id, amount=amount)
            s.save()
            return JsonResponse({'code':200,'info':'投资项目成功'})
        except Exception as e:
            print(e)
            return JsonResponse({'code':401,'info':'投资项目失败！！'})

#执行喜爱操作
class project_loveView(View):
    def post(self,request):
        #获取记录是否存在
        data = json.loads(request.body)
        project_id = data['project_id']
        user_id =data['user_id']
        oprate = data['oprate']
        if oprate == 'get_love':
            try:
                love2 = t_favorite.objects.get(project_id=project_id, user_id=user_id)
            except t_favorite.DoesNotExist:
                return JsonResponse({'code':200,'info':'喜爱不存在'})

            return JsonResponse({"code":201,'info':'喜爱已存在'})
        else:
            try:
                love = t_favorite.objects.get(project_id=project_id, user_id=user_id)
                #   如果存在，则移除当前记录
                love.delete()
                #并减少喜爱人数
                t = t_project.objects.get(project_id=project_id)
                t.kanhao = t.kanhao-1
                t.save()
                return JsonResponse({"code":200,'info':'已取消'})
            except t_favorite.DoesNotExist:
                love = t_favorite(project_id=project_id, user_id=user_id)
                love.save()
                #增加喜爱人数
                t = t_project.objects.get(project_id=project_id)
                t.kanhao = t.kanhao+1
                t.save()
                return JsonResponse({"code":200,'info':'已看好'})
            except Exception as e:
                print(e)
                return JsonResponse({'code':400,'info':'出现错误'})

#执行添加评论操作
class project_comment(View):
    def post(self,request):
        data = json.loads(request.body)
        project_id = data['project_id']
        user_id =data['user_id']
        connect = data['connect']
        #添加评论
        comment = t_comment(project_id=project_id, user_id=user_id, content=connect)
        comment.save()
        return JsonResponse({"code":200,"info":"评论成功"})

#获取评论
class get_comment(View):
    def get(self, request):
        #获取项目id
        project_id = request.GET.get('project_id')
        if not project_id:
            return JsonResponse({'code': 400, 'error': '缺少项目 ID'}, status=400)
        # 存储项目所有评论
        comments = t_comment.objects.filter(project_id=project_id).prefetch_related('replies__user')
        serializer = t_commentSerializer(comments, many=True)
        return JsonResponse({'code': 200, 'data': serializer.data})

#评论回复功能实现
class reply_comment(View):
    def post(self,request):
        data = json.loads(request.body)
        user_id = data['user_id']
        comment_id = data['comment_id']
        content = data['content']
        try:
            comment_reply_id = data['comment_reply_id']
            print(comment_reply_id)
        except KeyError:
            try:
                t = t_comment_reply(user_id=user_id, comment_id=comment_id, content=content)
                t.save()
                return JsonResponse({'code': 200, 'info': '评论成功'})
            except Exception as e:
                print(e)
                return JsonResponse({'code':401,'info':'出现错误'})

        #如果没有出现key错误，说明是添加子回复评论
        s = t_comment_reply(user_id=user_id, comment_id=comment_id, content=content,parent_id=comment_reply_id)
        s.save()

        return JsonResponse({'code':200,'info':'评论成功'})

#搜索功能实现
class search_project(View):
    def get(self, request):
        title = request.GET.get('title')
        print(title)
        if not title:
            return JsonResponse({'code': 400, 'info': '关键字不能为空！', 'data': []})

        # #使用orm的模糊查询
        # # 使用 ORM 的模糊查询
        # results = t_project.objects.filter(title__icontains=title,status=0).select_related('owner')
        # #序列化数据
        # projects = [t_project_Serializer(project).data for project in results]
        # #返回给前端
        # return JsonResponse({'code': 200, 'info': "已获取所有信息",'data':{
        #     'projects':projects
        # }})
        #用数据库中定义的过程
        try:
                #查询视图
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM vw_search_projects WHERE LOWER(title) LIKE :title", {'title': '%' + title.lower() + '%'})
                results = cursor.fetchall()

                #构建返回数据
                projects=[]
                for row in results:
                    project_data={
                        'project_id': row[0],
                        'title': row[1],
                        'category': row[2],
                        'goal_amount': row[3],
                        'raised_amount': row[4],
                        'start_time': row[5].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[5], datetime) else row[5],  # 转换 datetime
                        'end_time': row[6].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[6], datetime) else row[6],  # 转换 datetime
                        'status': row[7],
                        'description': row[8].read() if isinstance(row[8], cx_Oracle.LOB) else row[8],
                        'owner':{
                            'id': row[9],
                            'username': row[10],
                            'avatar': row[12],
                        },
                        'resources': row[13],
                        'image': row[14],
                        'kanhao': row[15],
                    }
                    projects.append(project_data)
            return JsonResponse({'code': 200, 'info': '查询成功', 'data': {'projects': projects}})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'info': '查询失败', 'error': str(e)})


#通过id获取类别名
class get_categroy_name(View):
    def get(self, request):
        categroy_id = request.GET.get('category_id')
        if not categroy_id:
            return JsonResponse({'code': 400, 'info': '关键字不能为空！', 'data': []})

        category = t_category.objects.get(category_id=categroy_id)
        #进行序列化
        return JsonResponse({'category': CategorySerializer(category).data}, safe=False)

    #通过类别名获取项目
    def post(self, request):
        data = json.loads(request.body)
        category_name = data['category_name']
        if not category_name:
            return JsonResponse({'code': 400, 'info': '关键字不能为空！', 'data': []})
        try:
            projects = t_project.objects.filter(category=category_name,status=0).select_related('owner')
            all_projects =[t_project_Serializer(project).data for project in projects]
        except t_category.DoesNotExist:
            return JsonResponse({'code':400,'info':'不存在相应类别的项目'})

        return JsonResponse({'code':200,'data':all_projects})

#通过时间段查询项目
class search_project_ByTime(View):
    def post(self,request):
        data = json.loads(request.body)
        start_time = data['start_time']
        end_time = data['end_time']
        category = data['category']
        minMoney = data['minMoney']
        maxMoney = data['maxMoney']
        print(start_time,end_time,category,minMoney,maxMoney)
        #如果没有在类别界面，则直接查询所有在目标时间段的项目
        if category == 'no':
            # 获取所有正在进行的项目
            all_project = t_project.objects.filter(status=0).select_related('owner')
            #如果有项目类别，则查询指定项目类别的指定时间段内的数据
            #根据传入的参数过滤数据
            if start_time and end_time:
                # 转换字符串为 datetime 对象
                start_time_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                # 校验时间范围
                if start_time_dt >= end_time_dt:
                    return JsonResponse({"code": 400, "message": "结束时间必须晚于开始时间"})
                all_project = all_project.filter(start_time__gte=start_time_dt, end_time__lte=end_time_dt)

            if minMoney>0 or maxMoney>0:
                if maxMoney<=0:
                    maxMoney = float('inf')
                all_project = all_project.filter(goal_amount__gte=minMoney, goal_amount__lte=maxMoney)

            #返回查询结果
            projects = [t_project_Serializer(project).data for project in all_project]
            return JsonResponse({'code':200, 'data':{
                'projects':projects
            }})

        else:
            # 查询指定范围内的项目
            all_project = t_project.objects.filter(status=0,category=category).select_related('owner')
            #根据传入的参数过滤数据
            if start_time and end_time:
                # 转换字符串为 datetime 对象
                start_time_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                # 校验时间范围
                if start_time_dt >= end_time_dt:
                    return JsonResponse({"code": 400, "message": "结束时间必须晚于开始时间"})
                all_project = all_project.filter(start_time__gte=start_time_dt, end_time__lte=end_time_dt)

            if minMoney>0 or maxMoney>0:
                if maxMoney<=0:
                    maxMoney = float('inf')
                all_project = all_project.filter(goal_amount__gte=minMoney, goal_amount__lte=maxMoney)

            #返回查询结果
            projects = [t_project_Serializer(project).data for project in all_project]
            return JsonResponse({'code':200, 'data':{
                'projects':projects
            }})

#文件资料上传
class project_upload_file(View):
    def post(self,request):
        #判断前端给的数据是否包含键值对
        if request.FILES.get('file'):
            file = request.FILES.get('file')
            user_id = request.POST.get('user_id')
            if not user_id:
                return JsonResponse({"code": 400, "info": "缺少用户ID"})
            try:
                # 生成保存路径
                sub_dir = f"project_resouse/user_{user_id}/"
                unique_filename = f"{uuid.uuid4().hex}_{file.name}"
                # 保存文件
                file_path = default_storage.save(
                    os.path.join(sub_dir, unique_filename),
                    ContentFile(file.read())
                )
                # 相对路径
                relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
                return JsonResponse({
                    "code": 200,
                    "info": "文件上传成功",
                    "file": relative_path,
                })
            except Exception as e:
                print(e)
                return JsonResponse({'code': 400, 'info': '文件上传出错'})
        elif request.FILES.get('image'):
            image = request.FILES.get('image')
            user_id = request.POST.get('user_id')
            if not user_id:
                return JsonResponse({"code": 400, "info": "缺少用户ID"})
            try:
                # 生成保存路径
                sub_dir = f"project_images/user_{user_id}/"
                unique_filename = f"{uuid.uuid4().hex}_{image.name}"
                # 保存文件
                file_path = default_storage.save(
                    os.path.join(sub_dir, unique_filename),
                    ContentFile(image.read())
                )
                # 相对路径
                relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
                return JsonResponse({
                    "code": 200,
                    "info": "图片上传成功",
                    "file": relative_path,
                })
            except Exception as e:
                print(e)
                return JsonResponse({'code': 400, 'info': '图片上传出错'})

        return JsonResponse({'code':400,'info':'没有相应文件传入'})

#文件资料删除
class project_delete_file(View):
    def post(self,request):
        #获取前端返回的文件路径
        file_path = request.POST.get('file_path')
        if not file_path:
            return JsonResponse({"code": 400, "message": "没有传入文件路径"})

        #拼接完整的文件路径
        #修改文件前的两个.
        file_path = file_path[3:]
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        #检查文件是否存在并删除
        if os.path.exists(full_path):
            # 检查路径是否在 MEDIA_ROOT 中
            if not full_path.startswith(settings.MEDIA_ROOT):
                return JsonResponse({"code": 403, "message": "文件路径不正确"})
            try:
                os.remove(full_path)
                return JsonResponse({"code": 200})
            except Exception as e:
                return JsonResponse({"code": 500, "info": f"删除文件失败: {str(e)}"})
        else:
            return JsonResponse({'code':404,'info':'文件不存在'})

#项目相关文件下载
def download_resource(request):
    # 获取文件相对路径
    file_path = request.GET.get('file_path')
    # 拼接成文件的绝对路径
    absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print(absolute_path)
    # 检查文件是否存在
    if not os.path.exists(absolute_path):
        return HttpResponse("文件不存在", status=404)
    # 检查文件是否可读
    if not os.access(absolute_path, os.R_OK):
        return HttpResponse("文件不可读", status=403)
    # 返回文件流
    try:
        #获取文件名和扩展名
        file_name = os.path.basename(file_path)
        mime_type,_ = guess_type(absolute_path)
        mime_type = mime_type or 'application/octet-stream'

        response = FileResponse(open(absolute_path, 'rb'))
        response['Content-Type'] =mime_type
        # 设置文件名，支持中文文件名
        response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
        return response
    except Exception as e:
        print(f"文件读取失败: {e}")
        return HttpResponse(f"文件读取失败: {str(e)}", status=500)


#组合查询
class seacher_group(View):
    def post(self,request):
        data = json.loads(request.body)
        title = data['title']
        start_time = data['start_time']
        end_time = data['end_time']
        category = data['category']
        minMoney = data['minMoney']
        maxMoney = data['maxMoney']

        #获取指定项目
        all_project = t_project.objects.filter(status=0,title__icontains=title).select_related('owner')
        if category:
            all_project = all_project.filter(category=category)
        if start_time and end_time:
            #转换字符串对象
            # 转换字符串为 datetime 对象
            start_time_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            # 校验时间范围
            if start_time_dt >= end_time_dt:
                return JsonResponse({"code": 400, "message": "结束时间必须晚于开始时间"})
            all_project = all_project.filter(start_time__gte=start_time_dt, end_time__lte=end_time_dt)

        if maxMoney>0 or minMoney>0:
            if maxMoney <= 0:
                maxMoney = float('inf')
            all_project = all_project.filter(goal_amount__gte=minMoney, goal_amount__lte=maxMoney)

        # 返回查询结果
        projects = [t_project_Serializer(project).data for project in all_project]
        return JsonResponse({'code': 200, 'data': {
            'projects': projects
        }})