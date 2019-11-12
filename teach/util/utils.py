from django import forms
import json
import os.path
import re
import ipykernel
import requests

from urllib.parse import urljoin
from notebook.notebookapp import list_running_servers

from teach.models import TaskAnswer

nb_frame = {
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.7.3",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 2,
}


def taskize_form(tasks):
    formset_out = forms.modelformset_factory(
        TaskAnswer, fields=("answertext", "task"), extra=len(tasks), max_num=len(tasks)
    )(
        queryset=TaskAnswer.objects.none(),
        initial=[{"answertext": "", "task": t.id} for t in tasks],
    )

    for ti, form in enumerate(formset_out):

        task = tasks[ti]

        rkind = task.restriction_kind
        choices = [(x, x) for x in task.restriction_detail.split(";")]

        if rkind == "none":
            form.fields["answertext"].widget = forms.TextInput(attrs={"required": True})
        elif rkind == "choice":
            form.fields["answertext"].widget = forms.RadioSelect(
                choices=choices, attrs={"required": True}
            )
        elif rkind == "number_of_choices":
            form.fields["answertext"].widget = forms.CheckboxSelectMultiple(
                choices=choices,
            )
        elif rkind == "number":
            form.fields["answertext"].widget = forms.NumberInput(
                attrs={"required": True}
            )

        form.fields["answertext"].help_text = task.text
        form.fields["answertext"].label = task.name
        form.fields["answertext"].initial = ""

        form.fields["task"].widget = forms.HiddenInput()
        form.fields["task"].initial = task.id

        form.data = {"image": task.imagelink}

    return formset_out


def get_notebook_name():
    """
    Return the full path of the jupyter notebook.
    """
    kernel_id = re.search(
        "kernel-(.*).json", ipykernel.connect.get_connection_file()
    ).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(
            urljoin(ss["url"], "api/sessions"), params={"token": ss.get("token", "")}
        )
        for nn in json.loads(response.text):
            if nn["kernel"]["id"] == kernel_id:
                relative_path = nn["notebook"]["path"]
                return os.path.join(ss["notebook_dir"], relative_path)
