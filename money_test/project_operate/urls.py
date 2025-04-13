from django.urls import path

from project_operate import views

urlpatterns=[
    path('investment',views.project_investment,name='investment'),
    path('love',views.project_loveView.as_view(),name='love'),
    path('pub_comment',views.project_comment.as_view(),name='pub_comment'),
    path('get_comment',views.get_comment.as_view(),name='get_comment'),
    path('reply_comment',views.reply_comment.as_view(),name='reply_comment'),
    path('search',views.search_project.as_view(),name='search_project'),
    path('categroy_name',views.get_categroy_name.as_view(),name='categroy_name'),
    path('search-ByTime',views.search_project_ByTime.as_view(),name='search_project_ByTime'),
    path('upload_file',views.project_upload_file.as_view(),name='upload_file'),
    path('delete_file',views.project_delete_file.as_view(),name='delete_file'),
    path('download_resource',views.download_resource,name='download_resource'),
    path('search_list',views.seacher_group.as_view(),name='search_project'),
]