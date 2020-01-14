from django.db import models
from teach.core.render_content import FormatParser


class ContentType(models.Model):
    """
    node
    """

    jelm_type = "node"
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.id


class Content(models.Model):
    """
    Content class, the basic building block for all courses
    - node
    """

    jelm_type = "node"
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50, primary_key=True)
    text = models.TextField(max_length=2000)

    format = models.CharField(
        max_length=10,
        choices=[(x, x) for x in FormatParser.format_choices],
        default=FormatParser.default_format,
    )

    content_type = models.ForeignKey(
        "ContentType", on_delete=models.SET_NULL, null=True
    )

    # TODO: possible citations

    def __str__(self):

        return "{}, {} - {} ({})".format(
            self.content_type, self.format, self.title, self.id
        )
