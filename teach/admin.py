from django.contrib import admin
from . import models
from django.forms import TextInput, Textarea
from django.db import models as dbmodels


# Register your models here.

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    ordering = ['topic','type','title']
    #formfield_overrides = {
        #models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        #dbmodels.TextField: {'widget': Textarea(attrs={'rows':20, 'cols':40})},
    #}
    pass

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Lecture)
class LectureAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Slide)
class SlideAdmin(admin.ModelAdmin):
    pass




@admin.register(models.CourseStructure)
class CourseStructureAdmin(admin.ModelAdmin):
    pass

@admin.register(models.AdditionalContent)
class AddContentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.LectureStructure)
class LectureStructureAdmin(admin.ModelAdmin):
    pass

@admin.register(models.SlideStructure)
class SlideStructureAdmin(admin.ModelAdmin):
    pass




# Functions for importing courses:
def import_course(course_loc):
    if 'rikicourses.' != course_loc[:12]:
        raise ValueError('import course from rikicourses')
    course_module = __import__(course_loc, fromlist=[''])
    
    course = models.Course(course_module.course_info['name'],
                           course_module.course_info['description'],
                           course_module.course_info['course_id'],
                           course_module.course_info['version'])
    
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