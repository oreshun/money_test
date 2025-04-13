import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from unicodedata import category

from project_test.models import t_category, CategorySerializer, t_project_review, t_project, t_project_Serializer


# Create your views here.
#项目类别相关操作
class Category_Operate(View):
    #如果是get方法，就返回所有类别给前端
    def get(self, request):
        all_category = t_category.objects.all()
        return JsonResponse({'all_category': CategorySerializer(all_category,many=True).data},safe=False)

    #
    def post(self, request):
        data = json.loads(request.body)
        operate = data['operate']
        category_name = data['category_name']
        print(operate, category_name)
        #如果前端给的添加类名，则进行类名添加操作
        if operate == '添加类名':
            try:
                # 检查数据库中是否存在数据
                category = t_category.objects.get(category_name=category_name)
                return JsonResponse({'code': 401, 'info': '类别已经存在，无需添加'})
            except t_category.DoesNotExist:
                # 数据不存在时新增
                try:
                    new_category = t_category(category_name=category_name)
                    new_category.save()
                    return JsonResponse({'code': 200, 'info': '类别添加成功'})
                except Exception as e:
                    print(e)
                    return JsonResponse({'code': 500, 'info': '类别添加失败，请稍后重试'})

        elif operate == '删除类名':
            try:
                category = t_category.objects.get(category_name=category_name)
                category.delete()
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500, 'info': '类别删除失败，请稍后重试'})

            return JsonResponse({'code': 200, 'info': '类别删除成功'})


#获取未审核的项目
class Get_project_no_pass(View):
    #当管理员点击审核项目的页面后，获取所有未审核的项目
    def get(self, request):
        #创建列表，存储项目
        projects = []
        #获取审核表里未审核的项目
        #select_related 是 Django ORM 提供的优化工具，用于提前加载外键关联的对象。它会通过 JOIN 查询 一次性获取主表和外键表的数据，避免多次查询。
        project_review = t_project_review.objects.filter(status='0').select_related('project__owner')
        #获得项目的详细信息
        for p in project_review:
            project = p.project#直接访问预加载的项目对象
            #将其进行序列化后存在列表中，一同返回给前端
            project_data = t_project_Serializer(project).data
            projects.append(project_data)

        #返回给前端
        return JsonResponse({'code': 200, 'info': "已获取所有信息",'data':{
            'projects':projects
        }})

    #当前端点击按钮
    def post(self, request):
        data = json.loads(request.body)
        project_id = data['project_id']
        operate = data['operate']
        reviewer_id = data['reviewer_id']
        #如果是通过，修改其审核状态
        if operate == 'project_pass':
            try:
                project_2 = t_project_review.objects.get(project_id=project_id)
                project_2.status = '1'
                project_2.reviewer_id = reviewer_id
                project_2.save()
            except Exception as e:
                print(e)
                return JsonResponse({"code":401,"info":"修改项目审核状态失败"})

            return JsonResponse({"code":200,"info":"通过项目"})

        elif operate == 'project_no_pass':
            try:
                project_2 = t_project_review.objects.get(project_id=project_id)
                project_2.status = '2'
                project_2.reviewer_id = reviewer_id
                project_2.save()
            except Exception as e:
                print(e)
                return JsonResponse({"code": 401, "info": "修改项目审核状态失败"})

            return JsonResponse({"code": 200, "info": "驳回项目"})


#获取已经审核过，并且通过审核的项目
class Get_project_pass(View):
    #获取项目
    def get(self, request):
        # 获取所有满足条件的项目
        projects_queryset = t_project.objects.filter(t_project_review__status='1',status='0').select_related('owner')
        # 序列化数据
        projects = [t_project_Serializer(project).data for project in projects_queryset]

        #返回给前端
        return JsonResponse({'code': 200, 'info': "已获取所有信息",'data':{
            'projects':projects
        }})

    def post(self, request):
        data = json.loads(request.body)
        project_id = data['project_id']
        try:
            project = t_project.objects.get(project_id=project_id)
            project_data = t_project_Serializer(project).data
        except Exception as e:
            print(e)
            return JsonResponse({'code':401,'info':'获取项目信息失败'})

        return JsonResponse({'code':200,'data':{
            'project':project_data
        }})

class turn_project(View):
    def post(self, request):
        data = json.loads(request.body)
        project_id = data['project_id']
        try:
            project = t_project.objects.get(project_id=project_id)
            project.status='2'
            project.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 401, 'info': '修改项目状态失败'})

        return JsonResponse({'code':200})

#项目发布
class project_pub(View):
    def post(self, request):
        # 解析 JSON 数据
        data = json.loads(request.body)
        #获取字段值
        title = data['title']
        category = data['category']
        goal_amount = data['goal_amount']
        description = data['description']
        user_id = data['user_id']
        project_file = data['project_file']
        image = data['image']
        start_time = data['project_time'][0]
        end_time = data['project_time'][1]
        #如果上传了文件，则进行路径处理
        if project_file:
            project_file = project_file[3:]
        if image:
            image = image[18:]
        try:
            #进行添加
            p = t_project(title=title,category=category,goal_amount=goal_amount,description=description,owner_id=user_id,resources=project_file,image=image,start_time=start_time,end_time=end_time)
            p.save()
            #在添加成功后进行审核,将由触发器进行
            return JsonResponse({'code':200})
        except Exception as e:
            print(e)
            JsonResponse({'code':401,'info':'项目添加失败'+str(e)})


