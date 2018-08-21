from django.urls import path
from . import views
from .create import logiccourse

app_name = 'teach'
urlpatterns = [
    path('', views.home, name='home'),
    path('course/<str:course_id>', views.course, name='course'),
    path('slideshow/<str:lecture_id>', views.slideshow, name='slideshow'),
    path('testcreate/logic',logiccourse,name='logiccreate'),
]