from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt

from teach.models.content_models import Content
from teach.models.organization_models import Course, Lecture, Slide, Topic

from teach.util import add_to_level


# @login_required
def home(request):
    return render(
        request,
        "teach/home.html",
        {"courses": Course.objects.all(), "topics": Topic.objects.all()},
    )


# @login_required
def course_view(request, course_id):
    course_inst = get_object_or_404(Course, id=course_id)
    course_structure = course_inst.coursestructure_set.order_by("ordernum")

    to_include = [
        content_type.name for content_type in course_inst.content_types_selected.all()
    ]

    topics = Topic.objects.filter(
        related_contents__in=Content.objects.filter(
            slide__in=Slide.objects.filter(
                lecture__in=Lecture.objects.filter(coursestructure__in=course_structure)
            )
        )
    ).distinct()

    return render(
        request,
        "teach/course.html",
        {
            "course_name": course_inst.name,
            "course_id": course_id,
            "course_structure": course_structure,
            "to_include": to_include,
            "quizes": course_inst.tasklists.all(),
            "topics": topics,
        },
    )


# @login_required
def contentshow(request, course_id, type_id):
    course_inst = get_object_or_404(Course, id=course_id)
    course_structure = course_inst.coursestructure_set.order_by("ordernum")
    # a little crazy list comprehension
    # collecting list of content for each lecture in
    # {'o':ordernum,'c':content} format
    scl = [
        {"o": content_dic["o"], "c": c}
        for content_dic in [
            {
                "o": cs.ordernum,
                "cl": [
                    ss.content
                    for ls in cs.lecture.lecturestructure_set.order_by(
                        "ordernum", "subordernum"
                    )
                    for ss in ls.slide.slidestructure_set.order_by("ordernum")
                ],
            }
            for cs in course_structure
        ]
        for c in content_dic["cl"]
    ]

    # additional content in list of dicts
    acl = [
        {"o": ac.afterlecture, "c": ac.content}
        for ac in course_inst.additionalcontent_set.order_by("afterlecture")
    ]

    level1 = {"name": type_id, "content": []}

    ordered_to_add = sorted(scl + acl, key=lambda x: x["o"])
    for content_dic in ordered_to_add:
        add_to_level(content_dic["c"], level1, "topic")

    return render(request, "teach/contentshow.html", {"level1": level1})


# @login_required
def topicshow(request, topic_id):
    contents = Content.objects.filter(topic__pk=topic_id).order_by("content_type")
    topic = get_object_or_404(Topic, id=topic_id)

    level1 = {"name": topic.name, "content": []}

    for elem in contents:
        add_to_level(elem, level1, "content_type")
    print(level1)
    return render(request, "teach/contentshow.html", {"level1": level1})


# @login_required
def slideshow(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    prevo = -1
    elements = []
    for lstructure in lecture.lecturestructure_set.order_by("ordernum", "subordernum"):
        if lstructure.multislide:
            if lstructure.ordernum == prevo:
                elements[-1]["subslides"].append(lstructure.slide)
            else:
                elements.append({"multislide": True, "subslides": [lstructure.slide]})
        else:
            elements.append({"multislide": False, "subslides": [lstructure.slide]})
        prevo = lstructure.ordernum
    return render(
        request,
        "teach/slideshow.html",
        {
            "title_slide": lecture.titleslide,
            "slideshow_title": lecture.title,
            "slideshow_elements": elements,
        },
    )


@xframe_options_exempt
def slide_view(request, slide_id):
    slide = get_object_or_404(Slide, id=slide_id)
    elements = [{"multislide": False, "subslides": [slide]}]

    return render(
        request,
        "teach/slideshow.html",
        {
            "title_slide": False,
            "slideshow_title": slide.title,
            "slideshow_elements": elements,
        },
    )
