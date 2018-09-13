from django.shortcuts import render, get_object_or_404
#from django.contrib.auth.decorators import login_required

from .models import Course,Lecture,Topic

#@login_required
def home(request):
    courses = Course.objects.get_queryset()
    return render(request, 'teach/home.html', {'courses': courses})

#@login_required
def course(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    course_structure = course.coursestructure_set.order_by('ordernum')
    to_include = [type.name for type in course.content_types_selected.all()]
    
    return render(request, 'teach/course.html',
                  {'course_name': course.name,
                   'course_id': course_id,
                   'course_structure': course_structure,
                   'to_include': to_include})

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