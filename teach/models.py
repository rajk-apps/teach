from django.db import models
import re

class Course(models.Model):
    """
    Course class
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30,primary_key=True)
    lectures = models.ManyToManyField('Lecture',through='CourseStructure')

    def __str__(self):
        return self.name
    
    def render(self):
        """
        Create the necessary html templates for the slides in the course
        in a folder within the templates
        """
        pass

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

class CourseStructure(models.Model):
    """
    Course structure class connecting lectures
    with courses
    """
    ordernum = models.PositiveIntegerField()
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

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

class Slide(models.Model):
    """
    Slide class
    """
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50,primary_key=True)
    layout = models.CharField(max_length=200)
    contents = models.ManyToManyField('Content',through='SlideStructure')

    hastitle = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def render(self):
        slides = self.slidestructure_set.order_by('ordernum')
        return eval(self.layout,{'s':slides})

class Content(models.Model):
    """
    Content class
    """
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50,primary_key=True)
    text = models.CharField(max_length=2000)
    
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
    
    related_content = models.ManyToManyField('Content')
    
    def __str__(self):
        return self.title

    def remove_animation(self):
        return re.sub('<!--.*?-->','',self.text)

class SlideStructure(models.Model):
    """
    Slide structure class connecting pieces of content
    with slides
    """
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    ordernum = models.PositiveIntegerField()
    animate = models.BooleanField(default=True)

    def __str__(self):
        return str(self.ordernum)

#Different structure, add later:

class Topic(models.Model):
    """
    Topic class
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30,primary_key=True)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    """
    Chapter class
    """
    name = models.CharField(max_length=200)
    id = models.CharField(max_length=50,primary_key=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

    def __str__(self):
        return self.name