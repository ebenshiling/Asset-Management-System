from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register',views.register, name="register"),
    path ('login',views.login, name="login"),
    path ('dashboard',views.dashboard, name="dashboard"),
    path ('logout',views.logout, name="logout"),
    
    
    #CRUD
    path('create-record',views.create_record, name="create-record"),
    path('update-record/<int:pk>',views.update_record, name="update-record"),
    path ('record/<int:pk>',views.singular_record, name="record"),
    path('delete-record/<int:pk>',views.delete_record, name="delete-record"),
    path('upload-excel',views.upload_excel, name="upload-excel"),
]