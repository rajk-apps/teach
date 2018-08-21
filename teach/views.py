from django.shortcuts import render, get_object_or_404
#from django.contrib.auth.decorators import login_required

from .models import Course,Lecture

#@login_required
def home(request):
    courses = Course.objects.get_queryset()
    return render(request, 'teach/home.html', {'courses': courses})

#@login_required
def course(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'teach/course.html', {'course': course})

#@login_required
def slideshow(request,lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    return render(request, 'teach/slideshow.html', {'lecture': lecture})