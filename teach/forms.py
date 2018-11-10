from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


###Task Forms

class AnswerForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user')
        task_for = kwargs.pop('task')
        sub = kwargs.pop('submission')
        super(AnswerForm, self).__init__(*args, **kwargs)
        
        self.fields['user'] = User.objects.get(id=user_id)
        self.fields['task'] = Task.objects.get(id=task_for)
        self.fields['submission'] = sub
        
    
    class Meta:
        model = TaskAnswer
        fields = ['answertext']
        
        labels = {
            'answertext': ('válasz'),
        }


