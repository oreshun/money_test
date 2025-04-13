from django.db import models
from rest_framework import serializers


# Create your models here.
#引入数据库模型
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,null=False)
    password = models.CharField(max_length=255,null=False)
    user_email = models.CharField(max_length=255,null=False)
    identify = models.CharField(max_length=255,null=False)
    user_birthday = models.DateField(null=True)
    phonenumber = models.CharField(max_length=11)
    avatar = models.CharField(max_length=255)
    status = models.IntegerField(null=False,default=0)
    register_time = models.DateField(auto_now_add=True)
    remark = models.CharField(max_length=255)

    class Meta:
        db_table = 't_user'

#用DRF框架解决user序列化
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#创建新的序列器，方便数据传递
class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','identify','avatar','status']
