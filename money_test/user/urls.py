from django.urls import path

from user import views

urlpatterns = [
    path('test', views.TestView.as_view(), name='test'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('uploadavatar', views.upload_avatarView.as_view(), name='upload_avatarView'),
    path('uploadinfomation',views.upload_user_infomationView.as_view(), name='upload_user_infomationView'),
]