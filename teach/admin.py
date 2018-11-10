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



#Tasks

@admin.register(models.TaskList)
class TaskListAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(models.UserSubmission)
class SubmissionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.TaskAnswer)
class TaskAnswerAdmin(admin.ModelAdmin):
    pass