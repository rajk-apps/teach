from django.db import models
from django.contrib.auth.models import User
import re
from random import shuffle


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
    
    tasklists = models.ManyToManyField('TaskList',blank=True)

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

#-------------------------------------
#-----------Tasks: -------------------
#-------------------------------------

class TaskList(models.Model):
    """
    TaskList class
    """
    id = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=150)
    
    tasks = models.ManyToManyField('Task',blank=True)
    
    num_sample = models.PositiveIntegerField(default=0)
    
    instant_answer = models.BooleanField(default=False)
        
    def __str__(self):
        return self.name + " - " + self.id
    
    def stats(self,user,
              take_kind='view'):
        """
        take_kind:view/wrong/all/remain/new
        """

        subs = self.usersubmission_set.filter(user=user,submitted=True)         
        alltasks = self.tasks.all()
        to_sample = self.num_sample
        
        answered = alltasks.filter(taskanswer__user = user.id)
        not_answered = alltasks.difference(answered)
        
        answers = TaskAnswer.objects.filter(user=user.id,
                                            task__in=answered)
        
        good_answered = answers.filter(score=1).values_list('task',flat=True)
        poor_answered = answers.values_list('task',flat=True).difference(
            good_answered)
    
        if take_kind == 'view':
            remaining = []
        elif take_kind == 'wrong':
            remaining = alltasks.filter(id__in=poor_answered)
        elif take_kind == 'all':
            remaining = alltasks
        elif take_kind == 'remain':
            remaining = alltasks.filter(id__in=
                 not_answered.values_list('id',flat=True
                      ).union(poor_answered))
        elif take_kind == 'new':
            remaining = alltasks.filter(id__in=
                 not_answered.values_list('id',flat=True
                      ))
        else:
            remaining = []

        if len(remaining) > to_sample:
            remaining = remaining.order_by('?')[:to_sample]
        
        
        quizstats = {'qnum':len(alltasks),
                     'tried':len(answered),
                     'good':len(good_answered),
                     'subnum':len(subs)}

        
        return quizstats,subs,remaining

    

class Task(models.Model):
    """
    Task class
    """
    id = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=150)
    text = models.TextField()
    
    restriction_kind = models.CharField(max_length=25,
        choices = [('none','none'),
                   ('choice','choice'),
                   ('number_of_choices','number_of_choices'),
                   ('number','number')],
        default='none')
    
    restriction_detail = models.TextField(null=True,blank=True)
    
    eval_kind = models.CharField(max_length=25,
        choices = [('manual','manual'),
                   ('accuracy','accuracy'),
                   ('pct_off','pct_off')],
        default='manual')
    
    eval_detail = models.TextField(null=True,blank=True)
    eval_transform = models.TextField(null=True,blank=True)

    answer = models.ManyToManyField(User,through='TaskAnswer')
    
    explanation = models.TextField(null=True,blank=True)
    
    imagelink = models.CharField(max_length=150,null=True,blank=True)
    
    def __str__(self):
        return self.name + " - " + self.restriction_kind + " - " + self.id

class UserSubmission(models.Model):

    tasklist = models.ForeignKey(TaskList,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    starttime = models.BigIntegerField()
    endtime = models.BigIntegerField(blank=True,null=True)
    submitted = models.BooleanField(default=False,blank=True)
    
    def __str__(self):
        
        return self.tasklist.name + " - " + self.user.username + \
     " - " + str(self.starttime)
     
    def stats(self):
        
        scoref = int(sum([t.score for t in self.taskanswer_set.all()]) \
                      * 100 / self.tasklist.num_sample)
        
        return {'duration': "%.1f" % ((self.endtime - self.starttime) / 60),
                'total_score': str(scoref) + "%"}

class TaskAnswer(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    submission = models.ForeignKey(UserSubmission,on_delete=models.CASCADE)

    needs_human = models.BooleanField(default=False,blank=True)

    answertext = models.TextField(null=True,blank=True)

    score = models.FloatField(null=True,blank=True)
    
    def answersplit(self):
        
        return self.answertext.split(';')
    
    def optionsplit(self):
        
        corrects = [x.strip() for x in self.task.eval_detail.split(';')]
        
        all_poss = [x.strip() for x in self.task.restriction_detail.split(';')]
        
        
        if len(all_poss) == 1:
            if all_poss[0] == "":
                return [{'corr':True, 'text':x} for x in corrects]
        
        return [{'corr':(x in corrects),'text':x} for x in all_poss]
    
    def evaluate_score(self):
        method = self.task.eval_kind
        rest_method = self.task.restriction_kind
        detail = self.task.eval_detail
        transforms = []
        try:
            transforms = self.task.eval_transform.split(';')
        except:
            pass
        
        transfuns = {'strip':lambda x: x.strip(),
                    'lower':lambda x: x.lower(),
                    '':lambda x: x}
        
        def itertranses(s,funs,fundict):
            for f in funs:
                s = fundict[f](s)
            return s
                
        
        if method == 'manual':
            self.score = 0
            self.needs_human = True
        elif method == 'accuracy':
            answers = set([itertranses(s,transforms,transfuns) for s
                           in self.answertext.split(';')])
            corr = set([itertranses(s,transforms,transfuns) for s
                           in detail.split(';')])
            if rest_method == 'choice' or rest_method == 'none' or rest_method == 'number':
                sc = len(answers & corr)
            else:
                allposs = set([itertranses(s,transforms,transfuns) for s
                               in self.task.restriction_detail.split(';')])
                sc = (len(answers & corr)+len(allposs - corr - answers)) \
                                                / len(allposs)
            self.score = sc
        else:
            self.score = (float(self.answertext) - float(detail))

####
#Organizing content topically:
####

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