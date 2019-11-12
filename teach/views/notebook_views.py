from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from teach.models import Course, Topic, Lecture, Slide, ContentType, Content
from teach.util.utils import nb_frame
from teach.core.notebook_parsing import ContentNotebook, SlideNotebook

import json


def content_nb_view(request, collection_id):
    coll = None
    for obj in [Course, Topic, Lecture, Slide, ContentType]:
        try:
            coll = obj.objects.get(pk=collection_id)
        except ObjectDoesNotExist:
            pass

    if isinstance(coll, Course):
        content_filter = {
            "slide__in": Slide.objects.filter(lecture__in=coll.lectures.all())
        }
    elif isinstance(coll, Topic):
        content_filter = {"topic": coll}
    elif isinstance(coll, Lecture):
        content_filter = {"slide__in": coll.slides.all()}
    elif isinstance(coll, Slide):
        content_filter = {"slide": coll}
    elif isinstance(coll, ContentType):
        content_filter = {"content_type": coll}
    else:
        content_filter = {}

    content_set = Content.objects.filter(**content_filter)

    nb_frame["cells"] = ContentNotebook(object_set=content_set).cell_list

    return HttpResponse(json.dumps(nb_frame))


def slide_nb_view(request, collection_id):
    coll = None
    for obj in [Course, Topic, Lecture, Slide, ContentType]:
        try:
            coll = obj.objects.get(pk=collection_id)
        except ObjectDoesNotExist:
            pass

    if isinstance(coll, Course):
        slide_filter = {"lecture__in": coll.lectures.all()}
    elif isinstance(coll, Topic):
        slide_filter = {"contents__in": Content.objects.filter(topic=coll)}
    elif isinstance(coll, Lecture):
        slide_filter = {"lecture": coll}
    elif isinstance(coll, Slide):
        slide_filter = {"pk": coll.pk}
    elif isinstance(coll, ContentType):
        slide_filter = {"contents__in": Content.objects.filter(content_type=coll)}
    else:
        slide_filter = {}

    slide_set = Slide.objects.filter(**slide_filter)

    nb_frame["cells"] = SlideNotebook(object_set=slide_set).cell_list

    return HttpResponse(json.dumps(nb_frame))
