from django import forms

from .models import TaskAnswer


def add_to_level(elem, l1):
    if l1['name'] == elem.type.name:
        added = False
        for l2 in l1['content']:
            if l2['name'] == elem.topic.name:
                if elem.id not in l2['eids']:
                    l2['content'].append(elem)
                    l2['eids'].append(elem.id)
                added = True
        if not added:
            l1['content'].append({'name': elem.topic.name,
                                  'description': elem.topic.description,
                                  'content': [elem],
                                  'eids': [elem.id]})


def taskize_form(tasks):
    formset_out = forms.modelformset_factory(TaskAnswer,
                                       fields=('answertext', 'task'),
                                       extra=len(tasks),
                                       max_num=len(tasks))(
        queryset=TaskAnswer.objects.none(),
        initial=
        [{'answertext': '', 'task': t.id} for t in tasks])

    for ti, form in enumerate(formset_out):

        task = tasks[ti]

        rkind = task.restriction_kind
        choices = [(x, x) for x in task.restriction_detail.split(';')]

        if rkind == 'none':
            form.fields['answertext'].widget = forms.TextInput(
                attrs={'required': True})
        elif rkind == 'choice':
            form.fields['answertext'].widget = forms.RadioSelect(
                choices=choices, attrs={'required': True}
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

        form.data = {'image': task.imagelink}

    return formset_out
