from django.urls import path

from project_test import views

app_name = 'project_test'

urlpatterns = [
    path('category', views.Category_Operate.as_view(), name='categroy'),
    path('getproject-nopass',views.Get_project_no_pass.as_view(), name='get_project_no_pass'),
    path('getproject-pass',views.Get_project_pass.as_view(), name='get_project_pass'),
    path('turn_project',views.turn_project.as_view(), name='turn_project'),
    path('add_project',views.project_pub.as_view(), name='add_project'),
]