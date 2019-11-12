from django.db import models
from django.contrib.auth.models import User


class TaskList(models.Model):
    """
    TaskList class
    node
    """
    jelm_type = 'node'

    id = models.CharField(max_length=30,
                          primary_key=True)
    name = models.CharField(max_length=150)
    
    tasks = models.ManyToManyField('Task',
                                   blank=True)
    
    num_sample = models.PositiveIntegerField(default=0)
    
    instant_answer = models.BooleanField(default=False)
        
    def __str__(self):
        return self.name + " - " + self.id
    
    def stats(self, user,
              take_kind='view'):
        """
        take_kind:view/wrong/all/remain/new
        """

        subs = self.usersubmission_set.filter(user=user,
                                              submitted=True)
        alltasks = self.tasks.all()
        to_sample = self.num_sample
        
        answered = alltasks.filter(taskanswer__user=user.id)
        not_answered = alltasks.difference(answered)
        
        answers = TaskAnswer.objects.filter(user=user.id,
                                            task__in=answered)
        
        good_answered = answers.filter(score=1).values_list('task',
                                                            flat=True)
        poor_answered = answers.values_list('task',
                                            flat=True).difference(
            good_answered)
    
        if take_kind == 'view':
            remaining = []
        elif take_kind == 'wrong':
            remaining = alltasks.filter(id__in=poor_answered)
        elif take_kind == 'all':
            remaining = alltasks
        elif take_kind == 'remain':
            remaining = alltasks.filter(
                id__in=not_answered.values_list('id',
                                                flat=True
                                                ).union(poor_answered))
        elif take_kind == 'new':
            remaining = alltasks.filter(
                id__in=not_answered.values_list('id',
                                                flat=True
                                                ))
        else:
            remaining = []

        if len(remaining) > to_sample:
            remaining = remaining.order_by('?')[:to_sample]

        quizstats = {'qnum': len(alltasks),
                     'tried': len(answered),
                     'good': len(good_answered),
                     'subnum': len(subs)}

        return quizstats, subs, remaining


class Task(models.Model):  # TODO: make this for programs/code/nice things
    # TODO: make this inherit content type
    """
    Task class
    node
    """
    jelm_type = 'node'

    id = models.CharField(max_length=30,
                          primary_key=True)
    name = models.CharField(max_length=150)
    text = models.TextField()
    
    restriction_kind = models.CharField(
        max_length=25,
        choices=[('none', 'none'),
                 ('choice', 'choice'),
                 ('number_of_choices', 'number_of_choices'),
                 ('number', 'number')],
        default='none')
    
    restriction_detail = models.TextField(null=True,
                                          blank=True)  # FIXME: some explanation here
    
    eval_kind = models.CharField(  # TODO: expand this and better choice handling
        max_length=25,
        choices=[('manual', 'manual'),
                 ('accuracy', 'accuracy'),
                 ('pct_off', 'pct_off')],
        default='manual')
    
    eval_detail = models.TextField(null=True,
                                   blank=True)
    eval_transform = models.TextField(null=True,
                                      blank=True)

    answer = models.ManyToManyField(User,
                                    through='TaskAnswer')
    
    explanation = models.TextField(null=True,
                                   blank=True)
    
    imagelink = models.CharField(max_length=150,
                                 null=True,
                                 blank=True)
    
    def __str__(self):
        return self.name + " - " + self.restriction_kind + " - " + self.id


class UserSubmission(models.Model):

    jelm_type = 'edge'

    tasklist = models.ForeignKey(TaskList,
                                 on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    starttime = models.BigIntegerField()
    endtime = models.BigIntegerField(blank=True,
                                     null=True)
    submitted = models.BooleanField(default=False,
                                    blank=True)
    
    def __str__(self):
        
        return self.tasklist.name + " - " + self.user.username + \
               " - " + str(self.starttime)
     
    def stats(self):
        
        scoref = int(sum([t.score for t in self.taskanswer_set.all()])
                     * 100 / self.tasklist.num_sample)
        
        return {'duration': "%.1f" % ((self.endtime - self.starttime) / 60),
                'total_score': str(scoref) + "%"}


class TaskAnswer(models.Model):

    jelm_type = 'node'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    submission = models.ForeignKey(UserSubmission,
                                   on_delete=models.CASCADE)

    needs_human = models.BooleanField(default=False,
                                      blank=True)

    answertext = models.TextField(null=True,
                                  blank=True)

    score = models.FloatField(null=True,
                              blank=True)
    
    def answersplit(self):
        
        return self.answertext.split(';')
    
    def optionsplit(self):
        
        corrects = [x.strip() for x in self.task.eval_detail.split(';')]
        
        all_poss = [x.strip() for x in self.task.restriction_detail.split(';')]  # TODO here is restriction_detail

        if len(all_poss) == 1:
            if all_poss[0] == "":
                return [{'corr': True,
                         'text': x} for x in corrects]
        
        return [{'corr': (x in corrects),
                 'text': x} for x in all_poss]
    
    def evaluate_score(self):  # TODO: WAAAAY TOO SIMPLE and also bad
        method = self.task.eval_kind
        rest_method = self.task.restriction_kind
        detail = self.task.eval_detail
        transforms = []
        try:
            transforms = self.task.eval_transform.split(';')
        except:
            pass
        
        transfuns = {'strip': lambda x: x.strip(),
                     'lower': lambda x: x.lower(),
                     '': lambda x: x}
        
        def itertranses(s, funs, fundict):
            for f in funs:
                s = fundict[f](s)
            return s

        if method == 'manual':
            self.score = 0
            self.needs_human = True
        elif method == 'accuracy':
            answers = set([itertranses(s, transforms, transfuns) for s
                           in self.answertext.split(';')])
            corr = set([itertranses(s,transforms,transfuns) for s
                           in detail.split(';')])
            if rest_method == 'choice' or rest_method == 'none' or rest_method == 'number':
                sc = len(answers & corr)
            else:
                allposs = set([itertranses(s,
                                           transforms,transfuns) for s
                               in self.task.restriction_detail.split(';')])

                sc = (len(answers & corr)+len(allposs - corr - answers)) \
                                                / len(allposs)
            self.score = sc
        else:
            self.score = (float(self.answertext) - float(detail))
