from django.db import models
import re

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

    def __str__(self):
        return self.name


class Content(models.Model):
    """
    Content class, the basic building block for all courses
    """
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50,primary_key=True)
    text = models.TextField(max_length=2000)
    
    MARKUP_CHOICES = [('md','md'),('html','html')]
    
    markup = models.CharField(max_length=4,
                              choices=MARKUP_CHOICES,
                              default='md')
    
    CONTENT_TYPES = [('def','Definition'),
                      ('list','List'),
                      ('task','Task'),
                      ('ex','Example'),
                      ('q','Question'),
                      ('misc','Misc')]
    
    type = models.CharField(max_length=4,
                            choices=CONTENT_TYPES,
                            default='misc')
    
    topic = models.ForeignKey('Topic',on_delete=models.SET_NULL,null=True)
    
    related_content = models.ManyToManyField('Content',blank=True)
    
    citation = models.CharField(max_length=300,default="",blank=True)
    citation_link = models.CharField(max_length=300,default="",blank=True)
    
    def __str__(self):
        return "%s - %s (%s)" % (self.type,self.title,self.id)

    def remove_animation(self):
        return re.sub('<!--.*?-->','',self.text)


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

class Slide(models.Model):
    """
    Slide class
    """
    
    DEF_LAYOUT = """[{'t':'r','ch':[
        {'t':'c','w':12,'ch':[
                {'t':'n','s':'',
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
    animate = models.BooleanField(default=True)
    print_title = models.BooleanField(default=False)

    def __str__(self):
        return " - ".join([self.slide.title,self.content.title,str(self.ordernum)])

#Organizing content topically:

class Topic(models.Model):
    """
    Topic class
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30,primary_key=True)

    def __str__(self):
        return self.name

