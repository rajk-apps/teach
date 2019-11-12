from django.db import models
from teach.core.render_content import FormatParser
import json


class Course(models.Model):
    """
    Course class
    node
    """

    jelm_type = "node"

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30, primary_key=True)
    version = models.CharField(max_length=15)

    lectures = models.ManyToManyField("Lecture", through="CourseStructure")
    tasklists = models.ManyToManyField("TaskList", blank=True)

    content_types_selected = models.ManyToManyField("ContentType", blank=True)

    def __str__(self):
        return self.name


class CourseStructure(models.Model):
    """
    Course structure class connecting lectures
    with courses
    edge
    """

    jelm_type = "edge"

    ordernum = models.PositiveIntegerField()
    lecture = models.ForeignKey("Lecture", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} ({})".format(
            self.course.name, self.lecture.title, self.ordernum
        )


class AdditionalLectureContent(models.Model):
    """
    Additinal content class connecting course
    with additional content to lectures
    node
    """

    jelm_type = "node"

    lecture = models.ManyToManyField("Lecture")
    content = models.ManyToManyField("Content")
    course = models.ManyToManyField("Course")

    ordernum = models.PositiveIntegerField(default=0)
    at_beginning = models.BooleanField(default=False)


class Lecture(models.Model):
    """
    Lecture class
    node
    """

    jelm_type = "node"
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    id = models.CharField(max_length=50, primary_key=True)
    slides = models.ManyToManyField("Slide", through="LectureStructure")

    titleslide = models.BooleanField(default=True)

    def __str__(self):
        return "Lecture: {}".format(self.title)


class LectureStructure(models.Model):
    """
    Lecture structure class connecting lectures
    with lectures
    edge
    """

    jelm_type = "edge"
    ordernum = models.FloatField()
    slide = models.ForeignKey("Slide", on_delete=models.CASCADE)
    lecture = models.ForeignKey("Lecture", on_delete=models.CASCADE)
    multislide = models.BooleanField(default=False)
    subordernum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return " - ".join([self.lecture.title, self.slide.title, str(self.ordernum)])

    def get_url_suffix(self):

        if self.multislide:
            return "#/%d/%d" % (self.ordernum, self.subordernum - 1)
        else:
            return "#/%d" % self.ordernum


def assign_to_layout_dic(dic, ss):

    if dic["tag"] == "leaf":
        dic["leaf"] = ss[int(dic["leaf"].replace("content-", ""))]
    else:
        for _d in dic["children"]:
            assign_to_layout_dic(_d, ss)


class Slide(models.Model):
    """
    Slide class
    node
    """

    jelm_type = "node"

    DEF_LAYOUT = json.dumps([{}], indent=2)

    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50, primary_key=True)
    layout = models.TextField(default=DEF_LAYOUT)
    contents = models.ManyToManyField("Content", through="SlideStructure")

    hastitle = models.BooleanField(default=True)

    def __str__(self):
        return self.id + " - " + self.title

    def render(self):
        slide_structures = self.slidestructure_set.order_by("ordernum")
        layout_dic = json.loads(self.layout)
        for dic in layout_dic:
            assign_to_layout_dic(dic, slide_structures)
        return layout_dic


class SlideStructure(models.Model):
    """
    Slide structure class connecting pieces of content
    with slides
    edge
    """

    jelm_type = "edge"
    slide = models.ForeignKey("Slide", on_delete=models.CASCADE)
    content = models.ForeignKey("Content", on_delete=models.CASCADE)
    ordernum = models.PositiveIntegerField()

    css_style = models.CharField(max_length=100, default="", blank=True)
    animate = models.BooleanField(default=True)
    print_title = models.BooleanField(default=False)
    fragment_no = models.SmallIntegerField(default=0)
    upto_level = models.SmallIntegerField(default=0)

    def __str__(self):
        return " - ".join([self.slide.title, self.content.title, str(self.ordernum)])

    def render(self):

        return FormatParser.render(self.content, self.upto_level, self.animate)
        return "FING"


class Topic(models.Model):
    """
    Topic class
    node
    """

    jelm_type = "node"
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    id = models.CharField(max_length=30, primary_key=True)

    related_contents = models.ManyToManyField("Content", blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.id)
