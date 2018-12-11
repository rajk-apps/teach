from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django import forms
import time
from copy import copy
from django.urls import reverse

from .models import *#Course,Lecture,Topic,Content,Task,TaskList
from teach.models import TaskAnswer

#@login_required
def home(request):
    courses = Course.objects.get_queryset()
    return render(request, 'teach/home.html',
                   {'courses': courses,
                    'topics':Topic.objects.all()})

#@login_required
def course(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    course_structure = course.coursestructure_set.order_by('ordernum')
    to_include = [type.name for type in course.content_types_selected.all()]
    topics = Topic.objects.filter(content__in = \
        Content.objects.filter(slide__in= \
             Slide.objects.filter(lecture__in = \
                 Lecture.objects.filter(coursestructure__in = course_structure)
                         ))).distinct()
            
    
    return render(request, 'teach/course.html',
                  {'course_name': course.name,
                   'course_id': course_id,
                   'course_structure': course_structure,
                   'to_include': to_include,
                   'quizes':course.tasklists.all(),
                   'topics': topics})

#@login_required
def contentshow(request,course_id,type_id):
    course = get_object_or_404(Course, id=course_id)
    course_structure = course.coursestructure_set.order_by('ordernum')
    #a little crazy list comprehension
    #collecting list of content for each lecture in
    #{'o':ordernum,'c':content} format
    scl = [ {'o':d['o'],'c':c} for d in
           [{'o':cs.ordernum,'cl':[ss.content for ls in
                cs.lecture.lecturestructure_set.order_by('ordernum',
                                                         'subordernum')
                for ss in
                ls.slide.slidestructure_set.order_by('ordernum')]} for cs in 
                course_structure] for c in d['cl']]
    
    
    #additional content in list of dicts
    acl = [{'o':ac.afterlecture,'c':ac.content} for ac in 
          course.additionalcontent_set.order_by('afterlecture')]
    
    
    level1 = {'name':type_id,'content':[]}
    
    def add_to_level(elem,l1):
        if l1['name'] == elem.type.name:
            added = False
            for l2 in l1['content']:
                if l2['name'] == elem.topic.name:
                    if elem.id not in l2['eids']:
                        l2['content'].append(elem)
                        l2['eids'].append(elem.id)
                    added = True
            if not added:
                l1['content'].append({'name':elem.topic.name,
                                      'description':elem.topic.description,
                                      'content':[elem],
                                      'eids':[elem.id]})
        
    ac_i = 0    
    sc_i = 0
    
    while ac_i < len(acl) and sc_i < len(scl):
        if acl[ac_i]['o'] < scl[sc_i]['o']:
            add_to_level(acl[ac_i]['c'],level1)
            ac_i += 1
        else:
            add_to_level(scl[sc_i]['c'],level1)
            sc_i += 1
    
    while ac_i < len(acl) or sc_i < len(scl):
        if ac_i < len(acl):
            add_to_level(acl[ac_i]['c'],level1)
            ac_i += 1
        else:
            add_to_level(scl[sc_i]['c'],level1)
            sc_i += 1
    
    
    return render(request, 'teach/contentshow.html',
                  {'level1':level1})

#@login_required
def topicshow(request,topic_id):
    contents = Content.objects.filter(topic__pk=topic_id).order_by('type')
    topic = get_object_or_404(Topic, id=topic_id)
    
    level1 = {'name':topic.name,'content':[]}
    
    for elem in contents:
        added = False
        for l2 in level1['content']:
            if l2['name'] == elem.type.name:
                l2['content'].append(elem)
                added = True
        if not added:
            level1['content'].append({'name':elem.type.name,
                                  'content':[elem]})
    
    
    return render(request, 'teach/contentshow.html',
                  {'level1':level1})


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


# ------- Tasks: ---------

@login_required
def take_quiz(request,tasklist_id,take_kind):
    
    if request.method == "POST":
        post_d = request.POST.copy()
        for key in request.POST:
            plist = request.POST.getlist(key)
            if len(plist) > 1:
                post_d[key] = ';'.join(plist)
        request.POST = post_d
        subid = request.POST.get('subid', '')
        formset = modelformset_factory(TaskAnswer,fields=('answertext','task'))(
            request.POST)
        if formset.is_valid():
            tas = formset.save(commit = False)
            for tanswer in tas:
                tanswer.user = request.user
                tanswer.submission_id = subid
                tanswer.evaluate_score()
                tanswer.save()
        sub = UserSubmission.objects.get(id=subid)
        sub.endtime = int(time.time())
        sub.submitted = True
        sub.save()
        return redirect(reverse('teach:view_quiz', 
                    kwargs={'tasklist_id':tasklist_id}) + '#' + str(sub.id))
        #return redirect('teach:view_quiz',tasklist_id=tasklist_id)
    
    root = get_object_or_404(TaskList, id=tasklist_id)
    
    quizstats,subs,remaining = root.stats(request.user,
                                          take_kind)

    submission = UserSubmission(user=request.user,
                                tasklist=root,
                                starttime=int(time.time()))
    submission.save()
    
    taskforms = taskize_form(remaining)
    
    return render(request, 'teach//quizes/take_quiz.html',
                  {'tasklist_name': root.name,
                   'quizstats': quizstats,
                   'taskforms': taskforms,
                   'subid':submission.id})



@login_required
def view_quiz(request,tasklist_id):
    
    root = get_object_or_404(TaskList, id=tasklist_id)
    
    quizstats,subs,remaining = root.stats(request.user,
                                          'view')
    sublist = [{'stats':sub.stats(),
                'answers':sub.taskanswer_set.all(),
                'id':sub.id} for sub in subs]
    
    return render(request,'teach/quizes/view_quiz.html',{'sublist':sublist,
                           'quizstats':quizstats,
                            'tasklist_name':root.name,
                            'tasklist_id':tasklist_id})




def taskize_form(tasks):
    
    formset_out = modelformset_factory(TaskAnswer,
                                fields=('answertext','task'),
                                extra=len(tasks),
                                max_num=len(tasks))(
                                queryset=TaskAnswer.objects.none(),
                                initial =
                                [{'answertext':'','task':t.id} for t in tasks])

    for ti,form in enumerate(formset_out):

        task = tasks[ti]
        
        rkind = task.restriction_kind
        choices = [(x,x) for x in task.restriction_detail.split(';')]
        
        
        if rkind == 'none':
            form.fields['answertext'].widget = forms.TextInput(
                attrs={'required': True})
        elif rkind == 'choice':
            form.fields['answertext'].widget = forms.RadioSelect(
                            choices=choices,attrs={'required': True}
                            )
        elif rkind == 'number_of_choices':
            form.fields['answertext'].widget = forms.CheckboxSelectMultiple(
                            choices=choices,
                            )
        elif rkind == 'number':
            form.fields['answertext'].widget = forms.NumberInput(
                attrs={'required': True})
    
        form.fields['answertext'].help_text = task.text
        form.fields['answertext'].label = task.name
        form.fields['answertext'].initial = ''
        
        form.fields['task'].widget = forms.HiddenInput()
        form.fields['task'].initial = task.id
        
        form.data = {'image':task.imagelink}
    
    return formset_out
