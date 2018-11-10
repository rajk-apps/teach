from django.contrib.auth.models import User
from django.forms import ModelForm
from django import template
from .models import


###Task Forms

class AnswerForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user')
        task_for = kwargs.pop('task')
        super(AnswerForm, self).__init__(*args, **kwargs)
        
        self.fields['user'] = User.objects.get(id=user_id)
        self.fields['task'] = User.objects.get(id=user_id)
        self.fields['answer'].queryset = task_for.get_options()
        
    
    class Meta:
        model = ChoiceTaskAnswer
        fields = ['answer']
        
        labels = {
            'answer': ('válasz'),
        }


register = template.Library()

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


