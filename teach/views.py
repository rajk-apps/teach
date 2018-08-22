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
    prevo = -1
    structures = []
    for lstructure in lecture.lecturestructure_set.order_by(
                       'ordernum','subordernum'):
        if lstructure.multislide:
            if lstructure.ordernum == prevo:
                structures[-1]['slides'].append(lstructure.slide)
            else:
                structures.append({'multislide':True,
                               'slides':[lstructure.slide]
                               })
        else:
            structures.append({'multislide':False,
                           'slide':lstructure.slide})
        prevo = lstructure.ordernum
    return render(request, 'teach/slideshow.html',
                  {'lecture_title': lecture.title,
                   'structures': structures
                   })