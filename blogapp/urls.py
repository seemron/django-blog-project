from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.request_access, name='signin'),
    path('', views.blog_list, name='blog_list'),
    path('post/<int:post_id>/', views.blog_detail, name='blog_detail'),
    # path('request-access/', views.request_access, name='request_access'),
    # path('request-post-access/<int:post_id>/', views.request_post_access, name='request_post_access'),
    path('request-access/', views.request_access, name='request_access'),

]

