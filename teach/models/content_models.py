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
                      ('iframe', 'iframe'),
                      ('img', 'img')]
    
    markup = models.CharField(max_length=10,
                              choices=MARKUP_CHOICES,
                              default='md')
    
    type = models.ForeignKey('ContentType',
                             on_delete=models.SET_NULL,
                             null=True)
    
    topic = models.ForeignKey('Topic',
                              on_delete=models.SET_NULL,
                              null=True)  # FIXME: make this many to many
    
    related_content = models.ManyToManyField('Content',
                                             blank=True)
    
    citation = models.CharField(max_length=300,
                                default="",
                                blank=True)

    citation_link = models.CharField(max_length=300,
                                     default="",
                                     blank=True)

    def __str__(self):

        if self.topic is None:
            return "Misc - %s - %s (%s)" % (self.type,
                                            self.title,
                                            self.id)
        else:
            return "%s - %s - %s (%s)" % (self.topic.name,
                                          self.type,
                                          self.title,
                                          self.id)

    def remove_animation(self):
        return re.sub(re.compile('<!--.*?-->'),
                      '',
                      str(self.text))

    def upto_level(self, level):
        out = self.text
        for ss in [x[0] for x in 
                   re.findall(re.compile('(\s*.*<!--.*?level=(\d+)*.*?-->)'),  # FIXME: this is probably wrong
                              str(self.text)) if float(x[1]) > level]:
            out = out.replace(ss, "")
        return out
    
    def get_occurrences(self):
        out = {}
        lss = [ls for s in self.slide_set.all()
               for ls in s.lecturestructure_set.all()]
        for ls in lss:
            lec = ls.lecture
            if lec.id in out.keys():
                out[lec.id]['slides'].append(ls)
            else:
                out[lec.id] = {'lec': lec,
                               'slides': [ls]}
        return out.values()
