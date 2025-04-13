from django.db import models
from rest_framework import serializers

from user.models import User, UserSerializer


# Create your models here.
#项目模型

class t_project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20,null=False,blank=False)
    category = models.CharField(max_length=20,null=False,blank=False)
    goal_amount = models.FloatField(null=False)
    raised_amount = models.FloatField(null=False,default=0)
    start_time = models.DateTimeField(null=False,auto_now_add=True)#创建时自动设置
    end_time = models.DateTimeField(null=False)
    status = models.CharField(max_length=1,null=False,default='0')
    description = models.TextField(null=True)
    owner = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    resources = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    kanhao = models.IntegerField(default=0)

    class Meta:
        db_table = 't_project'

#项目模型序列化
class t_project_Serializer(serializers.ModelSerializer):
    #嵌套序列化器
    owner = UserSerializer()
    class Meta:
        model = t_project
        fields = '__all__'

#项目类别模型
class t_category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=25,null=False,blank=False)

    class Meta:
        db_table = 't_category'

#类别序列化
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = t_category
        fields = '__all__'

#项目审核表模型
class t_project_review(models.Model):
    review_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(t_project,null=False,on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=1,null=False,default='0')
    review_time = models.DateTimeField(null=False,auto_now_add=True)
    comments = models.CharField(max_length=255)

    class Meta:
        db_table = 't_project_review'

#项目审核表的序列化
class t_project_review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = t_project_review
        fields = '__all__'


