from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
import time
from django.urls import reverse

from teach.models.task_models import TaskAnswer, TaskList, UserSubmission

from teach.util.utils import taskize_form


@login_required
def take_quiz(request, tasklist_id, take_kind):

    if request.method == "POST":
        post_d = request.POST.copy()
        for key in request.POST:
            plist = request.POST.getlist(key)
            if len(plist) > 1:
                post_d[key] = ";".join(plist)
        request.POST = post_d
        subid = request.POST.get("subid", "")
        formset = modelformset_factory(TaskAnswer, fields=("answertext", "task"))(
            request.POST
        )
        if formset.is_valid():
            tas = formset.save(commit=False)
            for tanswer in tas:
                tanswer.user = request.user
                tanswer.submission_id = subid
                tanswer.evaluate_score()
                tanswer.save()
        sub = UserSubmission.objects.get(id=subid)
        sub.endtime = int(time.time())
        sub.submitted = True
        sub.save()
        return redirect(
            reverse("teach:view_quiz", kwargs={"tasklist_id": tasklist_id})
            + "#"
            + str(sub.id)
        )

    root = get_object_or_404(TaskList, id=tasklist_id)

    quizstats, subs, remaining = root.stats(request.user, take_kind)

    submission = UserSubmission(
        user=request.user, tasklist=root, starttime=int(time.time())
    )
    submission.save()

    taskforms = taskize_form(remaining)

    return render(
        request,
        "teach//quizes/take_quiz.html",
        {
            "tasklist_name": root.name,
            "quizstats": quizstats,
            "taskforms": taskforms,
            "subid": submission.id,
        },
    )


@login_required
def view_quiz(request, tasklist_id):

    root = get_object_or_404(TaskList, id=tasklist_id)

    quizstats, subs, remaining = root.stats(request.user, "view")
    sublist = [
        {"stats": sub.stats(), "answers": sub.taskanswer_set.all(), "id": sub.id}
        for sub in subs
    ]

    return render(
        request,
        "teach/quizes/view_quiz.html",
        {
            "sublist": sublist,
            "quizstats": quizstats,
            "tasklist_name": root.name,
            "tasklist_id": tasklist_id,
        },
    )
