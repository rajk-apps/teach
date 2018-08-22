from django.contrib import admin
from . import models

# Register your models here.


# Functions for importing courses:
def import_course(course_loc):
    if 'rikicourses.' != course_loc[:12]:
        raise ValueError('import course from rikicourses')
    course_module = __import__(course_loc, fromlist=[''])
    
    course = models.Course(course_module.course_info['name'],
                           course_module.course_info['description'],
                           course_module.course_info['course_id'])
    
    try:
        past = models.Course.objects.get(pk=course.id)
        lecs = past.lectures.all()
        slides = [lec.slides.all() for lec in lecs]
        conts = [slide.contents.all() for slideset in slides for slide in slideset]
        past.delete()
        lecs.delete()
        [slide.delete() for slide in slides]
        [cont.delete() for cont in conts]
    except:
        print("This is most likely a new course")
    
    course.save()
    
    material = __import__(course_loc + '.material', fromlist=[''])
    material.create_material(course,models)