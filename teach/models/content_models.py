from django.db import models
import re


class ContentType(models.Model):
    id = models.CharField(max_length=5,
                          primary_key=True)
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return "%s (%s)" % (self.name,
                            self.id)


class Content(models.Model):
    """
    Content class, the basic building block for all courses
    """
    title = models.CharField(max_length=200)
    id = models.CharField(max_length=50,
                          primary_key=True)
    text = models.TextField(max_length=2000)
    
    MARKUP_CHOICES = [('md', 'md'),
                      ('html', 'html'),
                      ('py', 'py'),
                      ('iframe', 'iframe'),
                      ('img', 'img')]
    
    markup = models.CharField(max_length=10,
                              choices=MARKUP_CHOICES,
                              default='md')
    
    content_type = models.ForeignKey('ContentType',
                                     on_delete=models.SET_NULL,
                                     null=True)

    # TODO: make room for content relations and possible citations

    def __str__(self):

        return "{}, {} - {} ({})".format(self.content_type,
                                         self.markup,
                                         self.title,
                                         self.id)

    def remove_animation(self):
        return re.sub(re.compile('<!--.*?-->'),
                      '',
                      str(self.text))

    def upto_level(self, level):
        out = self.text
        for ss in [x[0] for x in 
                   re.findall(re.compile('(\s*.*<!--.*?level=(\d+)*.*?-->)'),  # FIXME: this is probably wrong, test it
                              str(self.text)) if float(x[1]) > level]:
            out = out.replace(ss, "")
        return out
