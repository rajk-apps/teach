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
    path('contentnb/<str:collection_id>/', views.content_nb_view,
         name='contentnb'),
    path('slidenb/<str:collection_id>/', views.slide_nb_view,
         name='slidenb'),
    path('slide/<str:slide_id>/', views.slide_view,
         name='slide'),
    path('status/', views.status,
         name='status'),
    path('export_jelm/', views.jelm_export,
         name='export_jelm'),
]
