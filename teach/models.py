from django.db import models
from django.contrib.auth.models import User
import re


class ContentType(models.Model):
    id = models.CharField(max_length=5,primary_key=True)
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return "%s (%s)" % (self.name,self.id)

class Content(models.Model):
    """
    Content class, the basic building block for all courses
    """
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50,primary_key=True)
    text = models.TextField(max_length=2000)
    
    MARKUP_CHOICES = [('md','md'),
                      ('html','html'),
                      ('iframe','iframe'),
                      ('img','img')]
    
    markup = models.CharField(max_length=10,
                              choices=MARKUP_CHOICES,
                              default='md')
    
    type = models.ForeignKey('ContentType',on_delete=models.SET_NULL,null=True)
    
    topic = models.ForeignKey('Topic',on_delete=models.SET_NULL,null=True)
    
    related_content = models.ManyToManyField('Content',blank=True)
    
    citation = models.CharField(max_length=300,default="",blank=True)
    citation_link = models.CharField(max_length=300,default="",blank=True)
    
        
    def __str__(self):
        if self.topic == None:
            return "Misc - %s - %s (%s)" % (self.type,self.title,self.id)
        else:
            return "%s - %s - %s (%s)" % (self.topic.name,self.type,self.title,self.id)

    def remove_animation(self):
        return re.sub('<!--.*?-->','',self.text)

    def upto_level(self,level):
        out = self.text
        for ss in [x[0] for x in 
                  re.findall('(\s*.*<!--.*?level=(\d+)*.*?-->)',
                     self.text) if float(x[1]) > level]:
            out = out.replace(ss,"")
        return out
    
    def get_occurrences(self):
        out = {}
        lss = [ls for s in self.slide_set.all() for ls in s.lecturestructure_set.all()]
        for ls in lss:
            lec = ls.lecture
            if lec.id in out.keys():
                out[lec.id]['slides'].append(ls)
            else:
                out[lec.id] = {'lec':lec,
                               'slides':[ls]}
        return out.values()
        

class Course(models.Model):
    """
    Course class
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30,primary_key=True)
    version = models.CharField(max_length=15)

    lectures = models.ManyToManyField('Lecture',through='CourseStructure')
    additional_content = models.ManyToManyField('Content',through='AdditionalContent')

    content_types_selected = models.ManyToManyField('ContentType',blank=True)

    def __str__(self):
        return self.name

#Classes organizing content into lectures:

class CourseStructure(models.Model):
    """
    Course structure class connecting lectures
    with courses
    """
    ordernum = models.PositiveIntegerField()
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str(self):
        return self.course.name + " - " + self.lecture.title
        
class AdditionalContent(models.Model):
    """
    Additinal content class connecting course
    with additional content
    """
    afterlecture = models.IntegerField()
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.course.name + " - " + self.content.title
    
class Lecture(models.Model):
    """
    Lecture class
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    id = models.CharField(max_length=50,primary_key=True)
    slides = models.ManyToManyField('Slide',through='LectureStructure')

    def __str__(self):
        return self.title

class LectureStructure(models.Model):
    """
    Lecture structure class connecting lectures
    with lectures
    """
    ordernum = models.PositiveIntegerField()
    slide = models.ForeignKey('Slide', on_delete=models.CASCADE)
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE)
    multislide = models.BooleanField(default=False)
    subordernum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return " - ".join([self.lecture.title,self.slide.title,str(self.ordernum)])
    
    def get_url_suffix(self):
        
        if self.multislide:
            return "#/%d/%d" % (self.ordernum,self.subordernum - 1)
        else:
            return "#/%d" % self.ordernum

class Slide(models.Model):
    """
    Slide class
    """
    
    DEF_LAYOUT = """[{'t':'r','ch':[
        {'t':'c','w':12,'ch':[
                {'t':'n',
                 'm':s[0]}
                ]}
            ]}
        ]"""
    
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50,primary_key=True)
    layout = models.TextField(default=DEF_LAYOUT)
    contents = models.ManyToManyField('Content',through='SlideStructure')

    hastitle = models.BooleanField(default=True)

    def __str__(self):
        return self.id + " - " + self.title
    
    def render(self):
        slides = self.slidestructure_set.order_by('ordernum')
        try:
            return eval(self.layout,{'s':slides})
        except:
            return []


class SlideStructure(models.Model):
    """
    Slide structure class connecting pieces of content
    with slides
    """
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    ordernum = models.PositiveIntegerField()
    
    css_style = models.CharField(max_length=100,default="",blank=True)
    animate = models.BooleanField(default=True)
    print_title = models.BooleanField(default=False)
    fragment_no = models.SmallIntegerField(default=0)
    upto_level = models.SmallIntegerField(default=0)

    def __str__(self):
        return " - ".join([self.slide.title,self.content.title,str(self.ordernum)])

    def render(self):
        
        if self.upto_level > 0:
            outtext = self.content.upto_level(self.upto_level)
        else:
            outtext = self.content.text
        
        if self.animate:
            return outtext
        else:
            return re.sub('<!--.*?-->','',outtext)

#------Tasks:

class Task(models.Model):
    """
    Task class
    """
    id = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=50)
    text = models.TextField()
    
    user_answer = models.ManyToManyField(User,through='TaskAnswer')
        
    def __str__(self):
        return self.type + " - " + self.id
    

class ChoiceTask(Task):
    
    wrong_options = models.ManyToManyField('TaskOption',related_name='wrong_option')
    correct_options = models.ManyToManyField('TaskOption',related_name='correct_option')



class TaskOption(models.Model):
    """
    Option for a task
    """
    id = models.CharField(max_length=30,primary_key=True)
    text = models.TextField()



class TaskAnswer(models.Model):
    """
    Answers by users
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    answer = models.ForeignKey(TaskOption,on_delete=models.CASCADE)


#Organizing content topically:

class Topic(models.Model):
    """
    Topic class
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30,primary_key=True)

    def __str__(self):
        return "%s (%s)" % (self.name,self.id)

#Course instances

class CourseInstance(models.Model):
    """
    A course instance with solutions for tasks, progress
    and all that
    """
    id = models.CharField(max_length=30,primary_key=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    students = models.ManyToManyField(User,through='CourseStudent',related_name='student')
    teachers = models.ManyToManyField(User,related_name='teacher')
    
class CourseStudent(models.Model):
    """
    Student performance in course
    """
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(CourseInstance,on_delete=models.CASCADE)