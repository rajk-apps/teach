from django.urls import path
from teach import views

app_name = 'teach'
urlpatterns = [
    path('', views.home,
         name='home'),
    path('course/<str:course_id>', views.course_view,
         name='course'),
    path('slideshow/<str:lecture_id>/', views.slideshow,
         name='slideshow'),
    path('take_quiz/<str:tasklist_id>/<str:take_kind>', views.take_quiz,
         name='take_quiz'),
    path('view_quiz/<str:tasklist_id>/', views.view_quiz,
         name='view_quiz'),
    path('content/<str:course_id>/<str:type_id>/', views.contentshow,
         name='contentshow'),
    path('topic/<str:topic_id>/', views.topicshow,
         name='topicshow'),
]
