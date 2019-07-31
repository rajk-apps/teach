from django.db import models
import re


class Course(models.Model):
    """
    Course class
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30, primary_key=True)
    version = models.CharField(max_length=15)

    lectures = models.ManyToManyField('Lecture', through='CourseStructure')
    additional_content = models.ManyToManyField('Content', through='AdditionalContent')
    tasklists = models.ManyToManyField('TaskList', blank=True)

    content_types_selected = models.ManyToManyField('ContentType', blank=True)

    def __str__(self):
        return self.name


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
    id = models.CharField(max_length=50, primary_key=True)
    slides = models.ManyToManyField('Slide', through='LectureStructure')

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
        return " - ".join([self.lecture.title,
                           self.slide.title,
                           str(self.ordernum)])
    
    def get_url_suffix(self):
        
        if self.multislide:
            return "#/%d/%d" % (self.ordernum,
                                self.subordernum - 1)
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
        ]"""  # TODO: make this better
    
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50, primary_key=True)
    layout = models.TextField(default=DEF_LAYOUT)
    contents = models.ManyToManyField('Content',
                                      through='SlideStructure')

    hastitle = models.BooleanField(default=True)

    def __str__(self):
        return self.id + " - " + self.title
    
    def render(self):
        slides = self.slidestructure_set.order_by('ordernum')
        try:
            return eval(self.layout,
                        {'s': slides})
        except:
            return []


class SlideStructure(models.Model):
    """
    Slide structure class connecting pieces of content
    with slides
    """
    slide = models.ForeignKey('Slide', on_delete=models.CASCADE)
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    ordernum = models.PositiveIntegerField()
    
    css_style = models.CharField(max_length=100,
                                 default="",
                                 blank=True)
    animate = models.BooleanField(default=True)
    print_title = models.BooleanField(default=False)
    fragment_no = models.SmallIntegerField(default=0)
    upto_level = models.SmallIntegerField(default=0)

    def __str__(self):
        return " - ".join([self.slide.title,
                           self.content.title,
                           str(self.ordernum)])

    def render(self):
        
        if self.upto_level > 0:
            outtext = self.content.upto_level(self.upto_level)
        else:
            outtext = self.content.text
        
        if self.animate:
            return outtext
        else:
            return re.sub('<!--.*?-->',
                          '',
                          outtext)


class Topic(models.Model):
    """
    Topic class
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30,primary_key=True)

    def __str__(self):
        return "%s (%s)" % (self.name,
                            self.id)
