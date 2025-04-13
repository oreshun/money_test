from django.db import models
from rest_framework import serializers
from project_test.models import t_project
from user.models import User, UserSerializer2


# Create your models here.
#创建投资记录表
class t_investment(models.Model):
    investment_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(t_project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    investment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_investment'

#创建喜爱表
class t_favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(t_project, on_delete=models.CASCADE)

    class Meta:
        db_table = 't_favorite'


#创建评论表
class t_comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(t_project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    comment_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 't_comment'


#创建评论回复表
class t_comment_reply(models.Model):
    comment_reply_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(t_comment, on_delete=models.CASCADE, related_name='replies')#回复的评论
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,related_name='children')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 't_comment_reply'

#评论回复表的序列化
class t_commentReplySerializer(serializers.ModelSerializer):
    user = UserSerializer2()
    parent_user_name = serializers.SerializerMethodField()
    class Meta:
        model = t_comment_reply
        fields = '__all__'

    def get_parent_user_name(self,obj):
        #递归嵌套子回复
        if obj.parent:
            return obj.parent.user.username
        return None


#评论表类别序列化
class t_commentSerializer(serializers.ModelSerializer):
    #嵌套序列器
    user = UserSerializer2()
    #关联回复
    replies = t_commentReplySerializer(many=True, read_only=True)
    class Meta:
        model = t_comment
        fields = '__all__'

    def get_replies(self, obj):
        # 获取评论的所有直接回复
        replies = t_comment_reply.objects.filter(comment=obj, parent__isnull=True)
        return t_commentReplySerializer(replies, many=True).data
