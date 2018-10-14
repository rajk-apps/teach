from django.urls import path
from . import views

app_name = 'teach'
urlpatterns = [
    path('', views.home, name='home'),
    path('course/<str:course_id>', views.course, name='course'),
    path('slideshow/<str:lecture_id>/', views.slideshow, name='slideshow'),
    path('content/<str:course_id>/<str:type_id>/', views.contentshow, name='contentshow'),
    path('topic/<str:topic_id>/', views.topicshow, name='topicshow'),
    path('tasklist/<str:tasklist_id>/', views.tasklist, name='tasklist'),
    path('task/<str:task_id>/', views.task, name='task'),
]